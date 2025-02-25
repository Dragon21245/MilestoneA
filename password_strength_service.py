import zmq
import json
import re

COMMON_PASSWORDS = {"password", "123456", "qwerty", "letmein", "admin", "welcome"}

def calculate_strength(password, username=None):
    """Evaluates password strength based on length, complexity, and common weaknesses."""
    score = 0
    feedback = []

    if len(password) >= 12:
        score += 40
    elif len(password) >= 8:
        score += 20
    else:
        feedback.append("Password is too short (min 8 characters).")

    if re.search(r"[A-Z]", password): score += 10
    else: feedback.append("Include at least one uppercase letter.")

    if re.search(r"[a-z]", password): score += 10
    else: feedback.append("Include at least one lowercase letter.")

    if re.search(r"[0-9]", password): score += 10
    else: feedback.append("Include at least one number.")

    if re.search(r"[\W_]", password): score += 10
    else: feedback.append("Include at least one special character.")

    if password.lower() in COMMON_PASSWORDS:
        score = 10
        feedback.append("This is a commonly used password. Choose something more secure.")

    if username and username.lower() in password.lower():
        score -= 10
        feedback.append("Password should not contain the username.")

    score = max(0, min(score, 100))
    is_secure = score >= 60

    return {"strength_score": score, "is_secure": is_secure, "feedback": feedback if feedback else ["Strong password!"]}

def start_microservice():
    """Starts the ZeroMQ password strength microservice."""
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("Password Strength Microservice is running...")

    while True:
        message = socket.recv_json()
        password = message.get("password", "")
        username = message.get("username", None)

        response = calculate_strength(password, username)
        socket.send_json(response)

if __name__ == "__main__":
    start_microservice()
