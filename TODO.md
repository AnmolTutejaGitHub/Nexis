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
- subaggent support
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

## On Gives Up too early:

graph.py has :
``` python
if not msg or not msg.get("tool_calls"):
    if msg and msg.get("content"):
        print_agent(msg["content"])
    return END
```
Any assistant reply with text but no tool call ends the turn. So when the model says "Let me now check X" without attaching a call, harness treats it as a final answer and stops.