from .models import ErrorClass

def classify(exc: Exception) -> ErrorClass:
    text = f"{type(exc).__name__}: {exc}".lower()
    if "permission" in text or "denied" in text:
        return ErrorClass.PERMISSION_DENIED
    if "not found" in text or "missing dependency" in text:
        return ErrorClass.DEPENDENCY_MISSING
    if "config" in text or "configuration" in text:
        return ErrorClass.CONFIG_INVALID
    if "timeout" in text or "connection" in text or "service" in text:
        return ErrorClass.SERVICE_DOWN
    if "security" in text or "unauthorized" in text or "forbidden" in text:
        return ErrorClass.SECURITY_BLOCKED
    if "data unavailable" in text or "no data" in text:
        return ErrorClass.DATA_UNAVAILABLE
    return ErrorClass.UNKNOWN
