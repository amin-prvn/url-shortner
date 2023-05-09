import secrets
import string

from app.api import models

def create_random_key(length: int = 5) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


async def create_unique_random_key() -> str:
    key = create_random_key()
    while await models.URL.get_by_key(key):
        key = create_random_key()
    return key
