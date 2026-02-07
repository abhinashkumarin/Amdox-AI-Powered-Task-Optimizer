# Login / Register
import hashlib, os

def hash_pwd(p):
    return hashlib.sha256(p.encode()).hexdigest()

def load_users():
    if not os.path.exists("data/users.txt"):
        return {}
    with open("data/users.txt") as f:
        return dict(line.strip().split(":") for line in f)

def register(u,p):
    os.makedirs("data", exist_ok=True)
    with open("data/users.txt","a") as f:
        f.write(f"{u}:{hash_pwd(p)}\n")

def login(u,p):
    return load_users().get(u) == hash_pwd(p)
