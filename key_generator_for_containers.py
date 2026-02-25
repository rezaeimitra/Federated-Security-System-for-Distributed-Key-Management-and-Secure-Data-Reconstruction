# key_generator_for_containers.py
import secrets
import binascii
from pathlib import Path

def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

# تولید دو سهم 16 بایتی
s2 = secrets.token_bytes(16)
s3 = secrets.token_bytes(16)

master = xor(s2, s3)

Path("node2").mkdir(exist_ok=True)
Path("node3").mkdir(exist_ok=True)
Path("node1").mkdir(exist_ok=True)

(node2_share := Path("node2/share.txt")).write_text(binascii.hexlify(s2).decode())
(node3_share := Path("node3/share.txt")).write_text(binascii.hexlify(s3).decode())

Path("master_key.txt").write_text(binascii.hexlify(master).decode())

print("Wrote shares:")
print("node2/share.txt ->", node2_share.read_text())
print("node3/share.txt ->", node3_share.read_text())
print("master_key.txt ->", Path("master_key.txt").read_text())
print("\n(Keep master_key.txt locally for validation; containers will only have their share files.)")
