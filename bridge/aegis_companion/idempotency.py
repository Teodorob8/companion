from threading import Lock

class DuplicateSuppressor:
    def __init__(self, max_items: int = 10000):
        self._seen: set[str] = set()
        self._order: list[str] = []
        self._max = max_items
        self._lock = Lock()

    def first_seen(self, key: str) -> bool:
        with self._lock:
            if key in self._seen:
                return False
            self._seen.add(key)
            self._order.append(key)
            if len(self._order) > self._max:
                old = self._order.pop(0)
                self._seen.discard(old)
            return True
