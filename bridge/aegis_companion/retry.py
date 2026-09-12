import random, time
from collections.abc import Callable

def bounded_retry(fn: Callable, attempts: int = 3, base_delay: float = 0.05):
    last = None
    for n in range(attempts):
        try:
            return fn()
        except Exception as exc:
            last = exc
            if n == attempts - 1:
                break
            time.sleep(base_delay * (2 ** n) + random.random() * base_delay)
    raise last
