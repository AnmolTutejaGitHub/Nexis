## TODO

- when ask to see something on Desktop it failed, required further prompting, fix system prompt for that
- multithreading for parallel tool calls
- steam response
- grep
- sometimes agent gives up too early, so need to add some kind of checks preventing that
- add prompt cashing 
- truncate tool results after a threshold
- better ui
- adding scratchboard/temp dir behaviour
- fix system prompt
- subagent support, system prompt to use subagents for codebase exploration
- mcp/skill/Agent.md support
- making compact func
- removing unecessary files
- session resume (local session write)
- / commands to clear, exit, compact, usage etc
- choosing model via cli without changing config
- install.sh and website to download
- publish as package, version release
- sandbox (it should be able to escape sandbox lol for the sake of game)
- for ls claude uses something like 
```bash
ls -la ~/.claude/ 2>/dev/null | head -40; echo "---PROJECT DIRS---"; ls ~/.claude/projects/ 2>/dev/null | head -20; echo "---COUNT---"; find ~/.claude/projects -name "*.jsonl" 2>/dev/null | wc -l; echo "---SIZE---"; du -sh ~/.claude/projects 2>/dev/null
```
so maybe i can implement similar behaviour instead of list_files
- current implementation has permissions at function level not at harness level, add that support, add support for `--dangerously-skip-permissions` too
- add support for events/ thinking planning/ `/goal` etc 
- add validation layer (either system prompt or harness level checks)
- add computer use skill
- implement better instruction set (using .md)
- add dynamic discovery for tools like claude code, give only function name 
- add observablity layer (logs etc)
- harness evalutaion 
- Read the opencode/codex codebase, figure out long-running tasks.
- See all tools used by claude code and see if anything i need
- system prompt contains no environment context, no cwd, no OS, no home path.
- calling get_repo_map many times, need to define a proper behaviour
- return get_repomap output as text instead of JSON. Every other tool now returns plain
  text; repomap is the last one wrapping its result in a nested JSON envelope, which is
  the most expensive shape of all — measured 184 tokens for tools/glob.py as JSON vs 80
  as text. One line per symbol also puts the line range next to the name so it can be
  passed straight to read_file_range:
      tools/glob.py (python)
      function   find_with_ripgrep                21-56
      function   glob_files                       69-98
      import     import os                        14
- notify the model when a file it has read is changed outside the harness. Claude Code
  injects a system message naming the file and showing the changed lines, so the model
  knows its view is stale and re-reads before editing. Nexis has no such signal and say "file changed since you
  read it, re-read first".
- define use of cd by bash and reset it to cwd once result is returned
- encode claude like bash usage in this harness
```bash
Bash(cd ~/Desktop/"Harness - Examples"/codex && rg -n "session_id" codex-rs/core/src/rollout/recorder.rs 2>/dev/null | head -10; echo "=== resume path ==="; rg -rn "fn resume" -g '*.rs' codex-rs/core/src/ | head -10)
```

## On multi-line paste firing one model call per line:

`user_input()` in `utils/print_utils.py` ends in `input()`, which returns a single line.
`agent.py`'s loop calls it once per turn, so pasting N lines is read as N separate user
prompts and fires N separate `graph.invoke` runs — one model call per pasted line.

The terminal delivers a paste as one fast burst, so it is separable from typing. Codex has
a `disable_paste_burst` config flag for the same problem.

Cheap fix — drain whatever is already buffered after the first line (20ms is longer than a
paste takes to land, shorter than a keystroke gap):

``` python
import select, sys

def read_paste_aware():
    lines = [input()]
    while select.select([sys.stdin], [], [], 0.02)[0]:
        line = sys.stdin.readline()
        if not line:
            break
        lines.append(line.rstrip("\n"))
    return "\n".join(lines)
```

Proper fix is `prompt_toolkit` (real bracketed-paste support), which would also cover
history, multi-line editing and `/` commands.

## On Gives Up too early:

graph.py has :
``` python
if not msg or not msg.get("tool_calls"):
    if msg and msg.get("content"):
        print_agent(msg["content"])
    return END
```
Any assistant reply with text but no tool call ends the turn. So when the model says "Let me now check X" without attaching a call, harness treats it as a final answer and stops.