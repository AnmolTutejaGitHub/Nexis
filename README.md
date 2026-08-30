# Nexis
<p align="center">
  <img src="https://socialify.git.ci/AnmolTutejaGithub/Nexis/image?font=Raleway&forks=1&issues=1&language=1&name=1&owner=1&pattern=Floating+Cogs&pulls=1&stargazers=1&theme=Dark" alt="Nexis" />
</p>
<p align="center">
  <a href="https://hits.sh/github.com/AnmolTutejaGitHub/Nexis/">
    <img src="https://hits.sh/github.com/AnmolTutejaGitHub/Nexis.svg?style=plastic&color=0077bf" alt="Hits"/>
  </a>
</p>

A coding agent that runs in your terminal. You describe a task in plain language; Nexis
reads the codebase, calls tools to search and edit it, and reports what it did.

https://github.com/user-attachments/assets/01498f79-b1e0-417f-b08a-2617c83a78bd

<p align="center"><sub>Asked to build itself a new tool: it reads the existing tools, writes the implementation, and registers it. (Sped up 2x.)</sub></p>

## How it works

A LangGraph state machine alternates between an `agent` node that calls the model and a
`tools` node that runs whatever it asked for, looping until the model replies without
requesting any tools.

- **`agent.py`** is the REPL: it reads your prompt, invokes the graph, and keeps the
  transcript.
- **`graph.py`** holds the two nodes above, plus the model call through LiteLLM.
- **`utils/run_tool_calls.py`** executes a turn's tool calls, batching the read-only ones
  into a thread pool and running the rest in order.
- **`events/`** is an event bus. The graph and tool runner emit `PreToolUse`,
  `PostToolUse`, `AgentMessage` and `Error`; listeners in `events/listeners/` handle
  rendering, approval prompts and logging. Nothing in the core writes to the screen.
- **`utils/ui/`** renders the terminal transcript. `tool_format.py` decides what each
  call and result says; `print_utils.py` decides where it lands.
- **`prompts/`** builds the system prompt, environment context (cwd, git branch,
  platform) and any `AGENTS.md` found in the project.

Because approval is a listener on the bus rather than a check inside each tool, adding a
tool that needs confirmation is one key in the registry, not a code change in the tool.

## Tools

| Tool | Description | Parallel | Asks first |
|---|---|:---:|:---:|
| `read_file` | Read a file from the start, up to a line limit | ✓ | |
| `read_file_range` | Read a specific line range | ✓ | |
| `glob_files` | Find files matching a glob pattern | ✓ | |
| `list_files` | List one directory, one level deep | ✓ | |
| `get_repomap` | Extract functions, classes and imports via Tree-sitter | ✓ | |
| `web_search` | Search the web via Tavily | ✓ | |
| `todo_write` | Maintain a task list for the current session | ✓ | |
| `edit_file` | One or more exact find-and-replaces, or whole-file overwrite | | ✓ |
| `create_path` | Create a file or directory | | |
| `delete_path` | Delete a file or directory, recursively | | ✓ |
| `bash_access` | Run a shell command | | ✓ |

Tools marked *parallel* are read-only and run concurrently when the model requests
several in one turn. Tools marked *asks first* stop for a y/n prompt, and `edit_file`
shows a diff before you decide.

Tree-sitter parsing covers 37 languages; see `tests/testing-repomap/`.

## Setup

**Requirements:** Python 3.12, [uv](https://docs.astral.sh/uv/), and an API key for a
model supported by [LiteLLM](https://docs.litellm.ai/docs/providers).

```bash
git clone https://github.com/AnmolTutejaGitHub/Nexis.git
cd Nexis
uv sync
```

`./setup.sh` does the below setups for you.

### Configure

```bash
cp .env.sample .env
```

### Run

```bash
uv run agent.py
```

Or install it once, from the Nexis directory, and `nexis` works from any directory in
that shell:

```bash
uv pip install -e .          # the "." is the Nexis directory, so run this from there
source /path/to/nexis/.venv/bin/activate   # path to .venv/bin/activate inside nexis
nexis                        # now works from anywhere
```

## Status

Early and actively being worked on. `TODO.md` tracks what is planned and what is
currently broken.

## License

MIT. See [LICENSE](LICENSE).
