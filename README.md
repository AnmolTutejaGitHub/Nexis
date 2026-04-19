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
git clone https://github.com/AnmolTuteworlds/Nexis.git
cd Nexis

# Create the virtual environment and install dependencies
uv sync
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

```bash
uv run agent.py
```

## License

MIT — see [LICENSE](LICENSE).
