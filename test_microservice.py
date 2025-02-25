import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

test_data = {
    "password": "P@ssw0rd123!",
    "username": "james_admin"
}

socket.send_json(test_data)
response = socket.recv_json()

print("Received Response:", json.dumps(response, indent=4))
