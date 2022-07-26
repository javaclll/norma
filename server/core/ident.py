import uuid

from core.redis import redis_client


def generate_new_identity() -> str:
    ident = uuid.uuid4()
    redis_client.set(str(ident), 1)
    return str(ident)


class Ident:
    def __init__(self, value, new) -> None:
        self.value = value
        self.new = new


async def get_ident(
    ident: str,
) -> Ident:
    if ident:
        ident_valid = redis_client.get(ident)
        if ident_valid != None:
            ident = str(ident)
            return Ident(value=ident, new=False)

    ident = generate_new_identity()
    return Ident(value=ident, new=True)
