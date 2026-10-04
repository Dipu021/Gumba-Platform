from getpass import getpass
from database.database import sessionlocal
from models.user import User
from security.hash_password import hash_password

username = input("Exact login username: ").strip()
password = getpass("New password: ")

with sessionlocal() as db:
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise ValueError("Username not found in this database")

    user.role = "admin"
    user.password_hash = hash_password(password)
    db.commit()

print("Admin account updated")