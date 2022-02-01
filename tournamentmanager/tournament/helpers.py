from base64 import urlsafe_b64decode, urlsafe_b64encode
from uuid import UUID


def uuid_to_slug(uuid) -> str:
    if isinstance(uuid, str):
        uuid = UUID(uuid)
    if not isinstance(uuid, UUID):
        raise ValueError('uuid must be a UUID instance or a string')
    return urlsafe_b64encode(uuid.bytes).decode('ascii').rstrip('=')


def slug_to_uuid(slug: str) -> UUID:
    if not isinstance(slug, str):
        raise ValueError('slug must be a string')
    slug += '=' * (-len(slug) % 4)
    return UUID(bytes=urlsafe_b64decode(slug))


def is_power_of_2(number: int) -> bool:
    if not isinstance(number, int):
        if isinstance(number, float):
            number = int(number)
        else:
            raise ValueError('number must be an integer')
    return number & (number - 1) == 0
