# create_admin.py — run once to create your initial admin account
from getpass import getpass

from database.database import sessionlocal
from models.user import User
from security.hash_password import hash_password


def main():
    username = input("Admin username: ").strip()
    email = input("Admin email: ").strip()
    password = getpass("Admin password: ")
    confirm_password = getpass("Confirm password: ")

    if not username or not email or not password:
        raise ValueError("Username, email, and password are required")

    if password != confirm_password:
        raise ValueError("Passwords do not match")

    with sessionlocal() as db:
        existing_user = (
            db.query(User)
            .filter((User.username == username) | (User.email == email))
            .first()
        )
        if existing_user:
            raise ValueError("That username or email is already registered")

        admin = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            role="admin",
        )
        db.add(admin)
        db.commit()

    print("Admin account created")


if __name__ == "__main__":
    main()