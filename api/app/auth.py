from datetime import datetime, timedelta
from passlib.context import CryptContext
import database

# add support for the algoritmes
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

# create a hashed password
def hash_password(plain_password):
    return pwd_context.hash(plain_password)

# verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# authenticate user
def authenticate_user(email: str, password: str):
    # see if user exist
    if database.user_exists(email=email) == False:
        return False,"Incorrect email!"
    # see if user is active
    if database.get_status_user(email=email) == 0:
        return False, "User is inactive!"
    # verify the password 
    if verify_password(plain_password=password, hashed_password=database.get_password(email=email)) == False:
        return False, "Incorrect password!"
    else:
        # login successfull
        return True, "Pass"