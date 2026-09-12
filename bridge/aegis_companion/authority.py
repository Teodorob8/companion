from .models import Mode, Capability

_ALLOWED = {
    Mode.RESEARCH: {Capability.READ_STATUS, Capability.READ_EVENTS, Capability.RUN_DIAGNOSTIC, Capability.SAFE_REPAIR},
    Mode.REPLAY: {Capability.READ_STATUS, Capability.READ_EVENTS, Capability.RUN_DIAGNOSTIC, Capability.SAFE_REPAIR},
    Mode.PAPER: {Capability.READ_STATUS, Capability.READ_EVENTS, Capability.RUN_DIAGNOSTIC, Capability.SAFE_REPAIR, Capability.PAPER_COMMAND},
}

def allowed(mode: Mode, capability: Capability, broker_state_known: bool = False) -> bool:
    if capability not in _ALLOWED[mode]:
        return False
    if capability == Capability.PAPER_COMMAND:
        return mode == Mode.PAPER and broker_state_known
    return True
