from pathlib import Path
import pytest

# Resolve the sibling source-sans repo
_SOURCE_SANS = Path(__file__).parent.parent.parent / "source-sans"
_UFO = _SOURCE_SANS / "Upright" / "Instances" / "Regular" / "font.ufo"


@pytest.fixture(scope="session")
def ufo_path():
    if not _UFO.exists():
        pytest.skip("source-sans repo not found at expected sibling path")
    return _UFO
