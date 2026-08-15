"""A place for the model to write temporary files."""

import tempfile

def scratchpad():
    """Return the session's scratch directory."""
    if not hasattr(scratchpad, "path"):
        scratchpad.path = tempfile.mkdtemp(prefix="nexis-scratchpad-")

    return scratchpad.path