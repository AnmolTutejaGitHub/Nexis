from dataclasses import dataclass

# Reference: https://code.claude.com/docs/en/hooks#hooks-reference

@dataclass
class Thinking:
    """Emitted when the model produces a thinking/reasoning trace."""

    text: str


@dataclass
class AgentMessage:
    text: str


@dataclass
class PreToolUse:
    """Emitted before a tool is executed. Approval gate - listeners return True/False."""

    tool_name: str
    tool_params: dict


@dataclass
class PostToolUse:
    """Emitted after a tool has executed with its result."""

    tool_name: str
    result: str


@dataclass
class Error:
    """Emitted when a step fails and the turn is given up on."""

    message: str
