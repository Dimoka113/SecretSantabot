import datetime
import random
import string
import psutil

def get_random_id():
    ALPHABET = string.digits + string.ascii_letters
    def to_base62(n: int) -> str:
        if n == 0: return ALPHABET[0]
        out = []
        base = len(ALPHABET)
        while n > 0:
            n, r = divmod(n, base)
            out.append(ALPHABET[r])
        return ''.join(reversed(out))

    def make_custom_timestamp_id(dt: datetime.datetime) -> int:
        time = dt.strftime("%Y%m%d%H%M%S%f")
        tail = random.randint(0, 10000) 
        ram = psutil.virtual_memory().used
        return int(f"{time}{ram}{tail}")

    return to_base62(make_custom_timestamp_id(datetime.datetime.now()))