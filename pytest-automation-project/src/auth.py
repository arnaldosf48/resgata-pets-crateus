def register_user(username, password):
    if not username or not password:
        return False
    return True

def login_user(username, password):
    if username == "testuser" and password == "testpass":
        return True
    return False