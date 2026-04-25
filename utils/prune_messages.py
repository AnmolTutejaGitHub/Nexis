import json
from typing import List,Dict
from config import config
from utils.observations import create_observation

def summarise_tool_result(tool_name: str,content: str):
    try:
        data = json.loads(content)

        if data.get("summary"):
            return content

        obs_id = create_observation(tool_name,data)

        if tool_name in ["read_file", "read_file_range"]:
            path = data.get("file") or data.get("path", "unknown")
            lines = len(data.get("content", "").splitlines())
            chars = len(data.get("content", ""))
            return json.dumps({
                "summary": f"read {lines} lines {chars} chars in {path}. use read_observation {obs_id} for full result"
            })

        if tool_name == "bash_access":
            stdout = data.get("stdout", "")
            stderr = data.get("stderr", "")
            code = data.get("returncode", "unknown")
            return json.dumps({
                "summary": f"ran command exit {code}, stdout {len(stdout)} chars stderr {len(stderr)} chars. use read_observation {obs_id} for full result"
            })
        
        if tool_name == "web_search":
            response = data.get("response", "")
            return json.dumps({
                "summary": f"web_search, response {len(str(response))} chars. use read_observation {obs_id} for full result"
            })
        
        if tool_name == "ask_human":
            return json.dumps({
                "summary": f"ask_human returned {len(content)} chars. use read_observation {obs_id} for full result"
            })
    
        if tool_name in  ["edit_file","update_file"]:
            path = data.get("file") or data.get("path", "unknown")
            return json.dumps({
                "summary": f"edited file {path}. use read_observation {obs_id} for full result"
            })
        
        if tool_name in ["list_files","get_repomap"]:
            return content

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

    if len(messages) <= config.RECENT_KEEP:
        return messages

    system = messages[0]
    old_messages = messages[1:-config.RECENT_KEEP]
    recent_messages = messages[-config.RECENT_KEEP:]

    for message in old_messages:
        if message.get("role") == "tool":
            tool_name = message.get("name")
            content = message.get("content")

            if tool_name and content and len(content) > 300:
                message["content"] = summarise_tool_result(tool_name, content)

    while total_chars([system] + old_messages + recent_messages) > config.MAX_CONTEXT_CHARS and old_messages:
        old_messages.pop(0)

    return [system] + old_messages + recent_messages
