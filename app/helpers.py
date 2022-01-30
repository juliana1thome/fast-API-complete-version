from passlib.context import CryptContext
from .config import settings

# Define my hash algorithm
passw_context = CryptContext(schemes=[settings.algorithm], deprecated="auto")


def hash(password: str):
    return passw_context.hash(password)


# This function takes the users password and hash it to check if it is the same hashed pass that I have in my db
def verify(plain_password, hashed_password):

    # It basically takes the hash algorithm and hashes the plain pass, and gets my db hashed pass, and it return it
    return passw_context.verify(plain_password, hashed_password)

