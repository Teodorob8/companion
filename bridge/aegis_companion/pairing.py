"""In-memory, one-time pairing primitives for the read-only Companion bridge."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import secrets


@dataclass
class PairingState:
    code_digest: str
    expires_at: datetime
    used: bool = False
    failures: int = 0
    locked_until: datetime | None = None


class PairingManager:
    def __init__(self, ttl_seconds: int = 600, max_failures: int = 5):
        self.ttl = timedelta(seconds=ttl_seconds)
        self.max_failures = max_failures
        self._state: PairingState | None = None

    @staticmethod
    def _digest(value: str) -> str:
        return hashlib.sha256(value.encode("ascii")).hexdigest()

    def issue_code(self, now: datetime | None = None) -> str:
        now = now or datetime.now(timezone.utc)
        code = f"{secrets.randbelow(1_000_000):06d}"
        self._state = PairingState(self._digest(code), now + self.ttl)
        return code

    def redeem(self, code: str, now: datetime | None = None) -> str | None:
        now = now or datetime.now(timezone.utc)
        state = self._state
        if state is None or state.used or now >= state.expires_at:
            return None
        if state.locked_until and now < state.locked_until:
            return None
        if not (len(code) == 6 and code.isascii() and code.isdigit()):
            state.failures += 1
        elif not secrets.compare_digest(self._digest(code), state.code_digest):
            state.failures += 1
        else:
            state.used = True
            return secrets.token_urlsafe(32)
        if state.failures >= self.max_failures:
            state.locked_until = now + timedelta(minutes=5)
        return None
