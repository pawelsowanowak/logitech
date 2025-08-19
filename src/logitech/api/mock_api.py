from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
]


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200


@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Invalid data"}), 400
    new_user = {"id": len(users) + 1, "name": data["name"], "email": data["email"]}
    users.append(new_user)
    return jsonify(new_user), 201


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    if user_id == 999:
        return jsonify({"error": "Internal Server Error"}), 500
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


if __name__ == "__main__":
    app.run(debug=True, port=5003)
