import datetime
import random
import string
import psutil

ALPHABET = string.digits + string.ascii_letters
BASE = len(ALPHABET)

def get_random_id(user: int|str = 0) -> str:
    def to_base62(n: int) -> str:
        if n == 0:
            return ALPHABET[0]

        out = []
        while n > 0:
            n, r = divmod(n, BASE)
            out.append(ALPHABET[r])
        return ''.join(reversed(out))

    now = datetime.datetime.now()
    time_part = int(now.strftime("%S%m%d%H%M%Y"))
    ram_used = psutil.virtual_memory().used

    if user:
        tail = random.randint(0, ram_used // 2)
        value = time_part + tail + int(user)
    else:
        tail = random.randint(0, ram_used)
        value = int(f"{time_part}{tail}")

    return to_base62(value)
