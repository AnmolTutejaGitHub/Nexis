import json
from typing import List,Dict


def summarise_tool_result(name: str,content: str):
    try:
        data = json.loads(content)

        if data.get("summary"):
            return content

        if name in ["read_file", "read_file_range", "get_repomap"]:
            path = data.get("file") or data.get("path", "unknown")
            return json.dumps({
                "summary": f"[Previously read: {path} — content omitted]"
            })

        elif name == "list_files":
            items = data.get("items", [])
            return json.dumps({
                "summary": f"[Listed {len(items)} items at {data.get('path', '')}]"
            })

        else:
            return json.dumps({
                "summary": f"[Truncated] {content[:300]}..."
            })

    except Exception:
        return content


def total_chars(messages: List[Dict]):
    total = 0
    for message in messages:
        for key, value in message.items():
            total += len(str(key))
            total += len(str(value))
    return total


def prune_messages(messages: List[Dict]):
    RECENT_KEEP = 6
    MAX_CONTEXT_CHARS = 50000

    if len(messages) <= RECENT_KEEP:
        return messages

    system = messages[0]
    old_messages = messages[1:-RECENT_KEEP]
    recent_messages = messages[-RECENT_KEEP:]

    for message in old_messages:
        if message.get("role") == "tool":
            tool_name = message.get("name")
            content = message.get("content")

            if tool_name and content and len(content) > 300:
                message["content"] = summarise_tool_result(tool_name, content)

    while total_chars([system] + old_messages + recent_messages) > MAX_CONTEXT_CHARS and old_messages:
        old_messages.pop(0)

    return [system] + old_messages + recent_messages