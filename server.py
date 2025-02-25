from flask import Flask, request, jsonify, render_template, send_from_directory
import zmq
import json
import os

app = Flask(__name__, static_folder=".")

def check_password_strength(password, username=""):
    """Send password to the ZeroMQ microservice and return strength details."""
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")  # Ensure your microservice is running

    request_data = {"password": password, "username": username}
    socket.send_json(request_data)
    response = socket.recv_json()
    return response

@app.route("/")
def index():
    """Serve index.html from the current directory."""
    return send_from_directory(".", "index.html")

@app.route("/check_password", methods=["POST"])
def password_check():
    """API endpoint to evaluate password strength."""
    data = request.get_json()
    password = data.get("password", "")
    username = data.get("username", "")

    if not password:
        return jsonify({"error": "Password required"}), 400

    result = check_password_strength(password, username)
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
