from pathlib import Path
from prompts.environment import environment_context

SYSTEM_PROMPT_PATH = Path(__file__).parent / "SYSTEM_PROMPT.md"

def system_prompt():
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").rstrip()

def build_system_prompt():
    return system_prompt() + "\n" + environment_context() + "\n"