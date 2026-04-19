# Nexis
<p align="center">
  <img src="https://socialify.git.ci/AnmolTutejaGithub/Nexis/image?font=Raleway&forks=1&issues=1&language=1&name=1&owner=1&pattern=Floating+Cogs&pulls=1&stargazers=1&theme=Dark" alt="Nexis" />
</p>
<p align="center">
  <a href="https://hits.sh/github.com/AnmolTutejaGitHub/Nexis/">
    <img src="https://hits.sh/github.com/AnmolTutejaGitHub/Nexis.svg?style=plastic&color=0077bf" alt="Hits"/>
  </a>
</p>

## Introduction

A coding agent that runs in your terminal. It can read, edit, search, and navigate codebases using tools.

### Tools

| Tool | Description |
|---|---|
| `read_file` / `read_file_range` | Read full files or specific line ranges |
| `edit_file` | Surgical find-and-replace edits |
| `update_file` | Overwrite a file with new content |
| `create_path` | Create files or directories |
| `delete_path` | Delete files or directories |
| `list_files` | List directory contents (one level deep) |
| `bash_access` | Execute shell commands |
| `web_search` | Search the web via Tavily |
| `semantic_search` | Vector-based codebase search |
| `get_repomap` | Extract code structure (functions, classes, imports) using Tree-sitter |

## Setup

### Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/) (recommended package manager)
- A Gemini API key (or any LLM provider supported by LiteLLM)
- A Tavily API key (for web search)

### Install

```bash
# Clone the repo
git clone https://github.com/AnmolTutejaGitHub/Nexis.git
cd Nexis

# Create the virtual environment and install dependencies
uv sync

# Install Nexis as an editable package (registers the `nexis` CLI command)
uv pip install -e .
```

### Configure

Copy the sample env file and add your keys:

```bash
cp .env.sample .env
```

```env
GEMINI_API_KEY=your-gemini-api-key
TAVILY_API_KEY=your-tavily-api-key
```

### Run

#### From the project directory

```bash
uv run agent.py
```

#### From anywhere (global CLI)

After installing with `uv pip install -e .`, activate the project's virtual environment to make the `nexis` command available globally:

```bash
source /path/to/Nexis/.venv/bin/activate 
# (source /Users/anmoltuteja/Desktop/Nexis/.venv/bin/activate in my case)
# now nexis works from anywhere
```

Now you can run Nexis from any directory:

```bash
nexis
```

## License

MIT — see [LICENSE](LICENSE).
