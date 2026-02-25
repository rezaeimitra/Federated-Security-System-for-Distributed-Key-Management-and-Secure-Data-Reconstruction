import os
import binascii
import requests
from flask import Flask, jsonify, request
from hashlib import sha256
import base64
from cryptography.fernet import Fernet
from datetime import datetime

app = Flask(__name__)

# =============================
# CONFIG
# =============================
NODE_NAME = os.environ.get("NODE_NAME", "Node")
NEIGHBORS = os.environ.get("NEIGHBORS", "")
NEIGHBORS = [n.strip() for n in NEIGHBORS.split(",") if n.strip()]

# Share file inside container
SHARE_PATH = "share.txt"

# Log directory (mounted from Windows)
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = "/app/logs/node.log"

# in-memory federation status
status_state = {
    "has_share": False,
    "share_sent": [],
    "share_received": [],
    "can_reconstruct": False,
}


# =============================
# LOGGING
# =============================
def log(msg):
    ts = datetime.utcnow().isoformat() + "Z"
    line = f"[{ts}] {msg}\n"
    with open(LOG_PATH, "a") as f:
        f.write(line)
    app.logger.info(line.strip())


# =============================
# HELPERS
# =============================
def read_share():
    if not os.path.exists(SHARE_PATH):
        return None
    hexs = open(SHARE_PATH, "r").read().strip()
    if not hexs:
        return None
    try:
        return binascii.unhexlify(hexs)
    except Exception:
        return None


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


# =============================
# ROUTES
# =============================
@app.route("/join", methods=["POST"])
def join():
    msg = request.json.get("message", "")
    log(f"[JOIN] Received join message: {msg}")
    return jsonify({"message": f"{NODE_NAME} joined"}), 200


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"node": NODE_NAME, "status": "active"})


@app.route("/federation-status", methods=["GET"])
def federation_status():
    own = read_share()
    status_state["has_share"] = bool(own)
    status_state["can_reconstruct"] = len(status_state["share_received"]) + (1 if own else 0) >= 2

    return jsonify({
        "node": NODE_NAME,
        "status": "active",
        "has_share": status_state["has_share"],
        "share_sent": status_state["share_sent"],
        "share_received": status_state["share_received"],
        "can_reconstruct": status_state["can_reconstruct"],
        "neighbors": NEIGHBORS
    })


@app.route("/send-share", methods=["GET"])
def send_share():
    s = read_share()
    if not s:
        log(f"[SEND] {NODE_NAME} has no share to send")
        return jsonify({"error": "no share"}), 404

    hexs = binascii.hexlify(s).decode()
    status_state["share_sent"].append(NODE_NAME)
    log(f"[SEND] {NODE_NAME} returned its share")
    return jsonify({"share": hexs})


@app.route("/request-and-reconstruct", methods=["POST"])
def request_and_reconstruct():
    shares = []

    # fetch from neighbors
    for n in NEIGHBORS:
        try:
            url = n.rstrip("/") + "/send-share"
            resp = requests.get(url, timeout=5)

            if resp.status_code == 200:
                j = resp.json()
                shares.append(binascii.unhexlify(j["share"]))
                status_state["share_received"].append(n)
                log(f"[REQUEST] got share from {n}")

        except Exception as e:
            log(f"[REQUEST] failed to get share from {n}: {e}")

    # include own share
    own = read_share()
    if own:
        shares.append(own)
        status_state["has_share"] = True

    if len(shares) < 2:
        log("[RECONSTRUCT] not enough shares to reconstruct")
        return jsonify({"error": "not enough shares", "have": len(shares)}), 400

    master = xor(shares[0], shares[1])
    log("[RECONSTRUCT] master key reconstructed")

    # derive Fernet key
    fernet_key = base64.urlsafe_b64encode(sha256(master).digest())
    f = Fernet(fernet_key)

    secure_path = "/secure/secure_partition.bin"
    out_path = "/secure/data.txt"

    if not os.path.exists(secure_path):
        log(f"[DECRYPT] secure partition missing: {secure_path}")
        return jsonify({"error": "secure_partition not found"}), 500

    try:
        with open(secure_path, "rb") as fh:
            encrypted = fh.read()
        decrypted = f.decrypt(encrypted)

        with open(out_path, "wb") as fo:
            fo.write(decrypted)

        log("[DECRYPT] secure partition decrypted")
        status_state["can_reconstruct"] = True

        return jsonify({"message": "reconstructed and decrypted", "out": out_path})

    except Exception as e:
        log(f"[DECRYPT] decrypt failed: {e}")
        return jsonify({"error": "decrypt failed", "exc": str(e)}), 500


# =============================
# BOOT
# =============================
if __name__ == "__main__":
    log(f"[BOOT] Starting {NODE_NAME} with neighbors {NEIGHBORS}")
    app.run(host="0.0.0.0", port=5000)
