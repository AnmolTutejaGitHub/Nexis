import os
import json
import tiktoken
from tools.code_navigation.repomap.get_repomap import get_repomap

encoding = tiktoken.encoding_for_model("gpt-4o")

def count_tokens(text):
    return len(encoding.encode(text, disallowed_special=()))

files = [
    "agent.py", "graph.py", "config.py",
    "tools/tool_registry.py", "tools/edit_file.py", "tools/read_file.py",
    "utils/prune_messages.py", "utils/observations.py",
    "tools/code_navigation/repomap/get_repomap.py",
]

for file in files:
    with open(file) as f:
        full_content = f.read()

    repomap = get_repomap(file)
    repomap_text = json.dumps(repomap)

    before = count_tokens(full_content)
    after = count_tokens(repomap_text)
    reduction = round((1 - after / before) * 100, 1)

    print(f"{file}: before={before} after={after} reduction={reduction}%")

# agent.py: before=140 after=170 reduction=-21.4%
# graph.py: before=515 after=345 reduction=33.0%
# config.py: before=193 after=64 reduction=66.8%
# tools/tool_registry.py: before=1978 after=392 reduction=80.2%
# tools/edit_file.py: before=510 after=75 reduction=85.3%
# tools/read_file.py: before=191 after=65 reduction=66.0%
# utils/prune_messages.py: before=672 after=190 reduction=71.7%
# utils/observations.py: before=285 after=159 reduction=44.2%