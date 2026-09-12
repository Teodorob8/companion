from bridge.aegis_companion.models import Mode, Capability
from bridge.aegis_companion.authority import allowed

def test_research_cannot_issue_paper_command():
    assert not allowed(Mode.RESEARCH, Capability.PAPER_COMMAND, broker_state_known=True)

def test_unknown_broker_state_blocks_paper_command():
    assert not allowed(Mode.PAPER, Capability.PAPER_COMMAND, broker_state_known=False)

def test_read_status_allowed():
    assert allowed(Mode.RESEARCH, Capability.READ_STATUS)
