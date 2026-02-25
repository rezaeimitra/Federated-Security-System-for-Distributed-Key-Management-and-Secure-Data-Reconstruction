# dashboard.py
from flask import Flask, render_template, jsonify, request
import requests
import os

app = Flask(__name__, template_folder="templates")

# آدرس نودها
NODES = [
    {"name": "Node1", "url": "http://localhost:5001"},
    {"name": "Node2", "url": "http://localhost:5002"},
    {"name": "Node3", "url": "http://localhost:5003"},
]

# تابع دریافت وضعیت نودها
def fetch_node_data():
    data = []
    for node in NODES:
        item = {"name": node["name"], "url": node["url"]}
        try:
            r1 = requests.get(f"{node['url']}/status", timeout=2)
            r2 = requests.get(f"{node['url']}/federation-status", timeout=2)

            item["status"] = r1.json().get("status", "unknown")
            fed = r2.json()

            item["has_share"] = fed.get("has_share", False)
            item["can_reconstruct"] = fed.get("can_reconstruct", False)
            item["share_sent"] = fed.get("share_sent", [])
            item["share_received"] = fed.get("share_received", [])
            item["neighbors"] = fed.get("neighbors", [])
        except Exception as e:
            item["status"] = "offline"
            item["error"] = str(e)

        data.append(item)

    return data


# Route صفحه داشبورد
@app.route("/")
def index():
    nodes = fetch_node_data()
    return render_template("index.html", nodes=nodes)


# Route برای دیدن لاگ یک نود
@app.route("/logs/<node_name>")
def read_logs(node_name):
    path = f"../{node_name}/logs/node.log"

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return jsonify({"node": node_name, "logs": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 404


# Route برای اجرای بازسازی از طریق نود 1
@app.route("/reconstruct", methods=["POST"])
def reconstruct():
    try:
        r = requests.post("http://localhost:5001/request-and-reconstruct")
        return r.json()
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(port=8000, debug=True)
