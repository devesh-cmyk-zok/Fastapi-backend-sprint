from passlib.context import CryptContext  # Used for hashing passwords

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # bcrypt is a hashing algorithm that is used to hash passwords, deprecated="auto" is used to automatically deprecate the old hashing algorithms

def hash_password(password: str) -> str:
    """
    Hashes a password using the bcrypt algorithm.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)  # hash the password using the bcrypt algorithm

def verify_password(plain_password: str, hashed_password: str):
    """
    Verifies a plain text password against a hashed password.

    Args:
        plain_password (str): The plain text password to be verified.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)  # verify the plain text password against the hashed password