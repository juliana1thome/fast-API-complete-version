from passlib.context import CryptContext
from .config import settings

# Define my hash algorithm
passw_context = CryptContext(schemes=[settings.algorithm], deprecated="auto")


def hash(password: str):
    return passw_context.hash(password)
