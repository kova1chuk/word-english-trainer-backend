#!/usr/bin/env python3
from app.core.security import get_password_hash
from app.db.models.user import User
from app.db.session import engine, Base
from sqlalchemy.orm import Session
import os
import sys

# make sure `app` is on PYTHONPATH
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(SCRIPT_DIR))


def main():
    # 1) Create the table if needed
    Base.metadata.create_all(bind=engine)
    print("✅ users table created")

    # 2) Seed an initial user (if not already present)
    with Session(engine) as session:
        email = "admin@example.com"
        if not session.query(User).filter_by(email=email).first():
            user = User(
                email=email,
                hashed_password=get_password_hash("ChangeMe123!")
            )
            session.add(user)
            session.commit()
            print(f"✅ seeded user {email}")
        else:
            print(f"ℹ️  user {email} already exists")


if __name__ == "__main__":
    main()
