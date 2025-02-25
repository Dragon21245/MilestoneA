# Password Strength Test Microservice

## Overview
This microservice evaluates password strength based on security best practices.
It runs as a **ZeroMQ-based service** and receives password evaluation requests.

## How to Set Up
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/password-strength-microservice.git
   cd password-strength-microservice

2. Install dependencies:

    pip install -r requirements.txt

3. Start the password strength microservice:

    python password_strength_service.py

## **A) How to Programmatically REQUEST Data**
To REQUEST data from the microservice, you must use **ZeroMQ** to establish a connection and send requests. Ensure you have **pyzmq** installed.

### **Steps to Send a Request**
1. Set up a **ZeroMQ Request socket** in your program.
2. Connect to the **microservice endpoint** at `"tcp://localhost:5555"`.
3. Use **`send_json()`** to send a request with the password and optional username.
4. Wait for the response.

### **Example Request (Python)**
```python
import zmq
import json

# Set up ZeroMQ request socket
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Request data format
request_data = {
    "password": "SecurePass123!",
    "username": "james_admin"
}

# Send the request
socket.send_json(request_data)

# Receive response
response = socket.recv_json()
print("Password Strength Response:", response)
```

B) How to Programmatically RECEIVE Data
To RECEIVE data from the microservice, you must listen for the response after sending a request.

Steps to Receive Data
1. After sending a request via ZeroMQ, the microservice processes the password.
2. It returns a JSON response containing:
strength_score (0-100): A numeric representation of password strength.
is_secure (Boolean): Whether the password meets security criteria.
feedback (List of strings): Suggestions for improving password security.

Example Response Handling (Python)
```
response = socket.recv_json()
print("Password Strength:", response["strength_score"])
print("Is Secure:", response["is_secure"])
print("Feedback:", response["feedback"])

Example Response Data (JSON)
{
    "strength_score": 75,
    "is_secure": true,
    "feedback": ["Strong password!"]
}
