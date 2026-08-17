# REFERENCES :
# https://github.com/anomalyco/opencode/blob/4643e65ad6/packages/opencode/src/tool/todo.ts
# https://github.com/anomalyco/opencode/blob/4643e65ad6/packages/schema/src/session-todo.ts
# https://github.com/anomalyco/opencode/blob/4643e65ad6/packages/opencode/src/tool/todowrite.txt

from pathlib import Path

DESCRIPTION = (Path(__file__).parent / "todowrite.txt").read_text(encoding="utf-8").strip()
STATUSES = ("pending", "in_progress", "blocked", "completed", "dropped")

_todos = []

def _validate(todos):
    if not isinstance(todos, list):
        return "todos must be a list"

    if len(todos) == 0:
        return "todos must not be empty"

    in_progress = 0

    for todo in todos:
        if not isinstance(todo, dict):
            return "each todo must be an object with content and status"

        content = todo.get("content", "")
        if not content.strip():
            return "every todo needs a non empty content"

        status = todo.get("status")
        if status not in STATUSES:
            return "status must be one of " + ", ".join(STATUSES)

        if status == "in_progress":
            in_progress += 1

    if in_progress > 1:
        return f"only one todo may be in_progress at a time (got {in_progress})"

    return None


def _render(todos):
    """Render as eg: `1. [pending] write the test`."""
    lines = []
    position = 1

    for todo in todos:
        lines.append(f"{position}. [{todo['status']}] {todo['content']}")
        position += 1

    return "\n".join(lines)


def todo_write(todos):
    """Replace the task list and send it back so the llm can see it."""
    error = _validate(todos)
    if error:
        return f"Error: {error}"

    _todos[:] = todos # replaces content
    return _render(_todos)


def todos():
    return _todos