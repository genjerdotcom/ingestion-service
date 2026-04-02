import os
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

CUSTOMERS_FILE = "data/customers.json"


def standard_response(data=None, message="success", status=200):
    return jsonify({
        "status": "success",
        "message": message,
        "data": data
    }), status


def stream_customers(start=0, limit=10):
    with open(CUSTOMERS_FILE) as f:
        buffer = ""
        in_array = False
        count = 0
        for line in f:
            line = line.strip()
            if line.startswith("["):
                in_array = True
                line = line[1:]
            if line.endswith("]"):
                line = line[:-1]
            if not line:
                continue
            buffer += line
            if buffer.endswith("},") or buffer.endswith("}"):
                item_str = buffer.rstrip(",")
                try:
                    item = json.loads(item_str)
                except json.JSONDecodeError:
                    buffer = ""
                    continue
                buffer = ""
                if count >= start and count < start + limit:
                    yield item
                count += 1
        return


@app.route("/")
def root():
    return standard_response(message="ok")

@app.route("/api/health")
def health():
    return standard_response(message="ok")

@app.route("/api/customers")
def get_customers():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    start = (page - 1) * limit

    customers_list = list(stream_customers(start, limit))

    total = sum(1 for _ in stream_customers(0, float("inf")))

    return jsonify({
        "data": customers_list,
        "total": total,
        "page": page,
        "limit": limit
    })

@app.route("/api/customers/<customer_id>")
def get_customer(customer_id):
    for c in stream_customers(0, float("inf")):
        if c["customer_id"] == customer_id:
            return standard_response(c)
    return standard_response(None, "Customer not found", 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("FLASK_PORT", 5000))