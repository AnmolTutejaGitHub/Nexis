from pathlib import Path
from prompts.environment import environment_context
from prompts import agents_md

SYSTEM_PROMPT_PATH = Path(__file__).parent / "SYSTEM_PROMPT.md"

def system_prompt():
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").rstrip()

def build_system_prompt():
    parts = [system_prompt(), environment_context(), agents_md.render()]
    return "\n".join(part for part in parts if part) + "\n"