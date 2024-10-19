import argparse
from database import SessionLocal, engine
from db_models import User, Role
from database import Base
from passlib.context import CryptContext

Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def add_admin(name: str, username: str, password: str):
    db = SessionLocal()
    try:
        existing_admin = db.query(User).filter(User.username == username, User.role == Role.admin).first()
        if existing_admin:
            print(f"Admin with username '{username}' already exists.")
            return

        hashed_password = pwd_context.hash(password)
        new_admin = User(name=name, username=username, password=hashed_password, role=Role.admin)
        db.add(new_admin)
        db.commit()
        print(f"Admin '{name}' added successfully.")
    except Exception as e:
        print(f"Error adding admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add new admin user to the database.")
    parser.add_argument("name", type=str, help="The name of the admin.")
    parser.add_argument("username", type=str, help="The username for the admin.")
    parser.add_argument("password", type=str, help="The password for the admin.")
    args = parser.parse_args()
    add_admin(args.name, args.username, args.password)
