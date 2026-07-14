# READ WRITE SEARCH tool for open-webui

A local file management tool for [Open WebUI](https://openwebui.com/), giving an LLM (via Ollama) the ability to read, write, create, delete, and search files inside a sandboxed directory on your machine — with a path-traversal guard so the model can't escape that sandbox.

Built as a `Tools` class for Open WebUI's native Tool system, running against a locally hosted model (tested with `qwen3.5:4b` via Ollama).

## Why

Giving an LLM raw filesystem access is risky — a model can be tricked (or can simply hallucinate) into passing a filename like `../../../../etc/passwd`. This tool constrains every file operation to a single base folder (`~/castle/` by default) and validates every path before touching disk, so no operation can resolve to anywhere outside that folder.

## Demo Video

[vid.webm]https://github.com/Mechanisium/rws_tool_open-webui/raw/main/demo/vid.webm

## Features

| Method | Description |
|---|---|
| `reader(filename)` | Read and return a file's contents as a list of lines |
| `writer(filename, content)` | Overwrite a file's contents from scratch |
| `appender(filename, content)` | Append content to an existing file |
| `creater(filename)` | Create a new, empty file (fails if it already exists) |
| `remover(filename)` | Delete a file |
| `directory_creater(dir_name)` | Create a new directory |
| `directory_remover(dir_name)` | Remove a directory (must be empty) |
| `list_directory(dir_name=".")` | List a directory's contents, split into `dir` and `file` lists |
| `search(filename)` | Recursively search the sandbox tree for a file by name |
| `safe_path(relative_path)` | Internal helper — resolves and validates a path against the sandbox root |

## Security

Every method routes user-supplied filenames/paths through `safe_path()` before touching the filesystem:

1. `os.path.abspath()` resolves the path to its true absolute destination, collapsing any `.`/`..` segments.
2. `os.path.commonpath()` checks whether that resolved destination still sits inside the sandboxed base folder.
3. If it doesn't, a `ValueError` is raised and the operation is refused — no file is read, written, or deleted.

This blocks path-traversal attempts (e.g. `"../../etc/passwd"`) while still allowing legitimate nested paths (e.g. `"notes/today.txt"`) within the sandbox.

## Setup

1. Requires Open WebUI running natively or via Docker, with a model available through Ollama.
2. In Open WebUI, go to **Workspace → Tools → Create New Tool**.
3. Paste in `r-w-s_tool_open-webui.py`.
4. Under the tool's **Valves**, set `base_path` to whichever folder you want the model to be sandboxed to (defaults to `~/castle/`).
5. Enable the tool on your model of choice and start prompting — e.g. *"create a file called notes.txt and write 'hello' into it."*

## Known limitations / roadmap

- `list_directory` currently returns absolute paths in `dir_path`, which works but is a little more revealing than strictly necessary — could be changed to relative paths.
- No content-based search yet (`search` currently matches filenames only).
- Planned: rewrite as a standalone MCP server (using FastMCP) for portability across MCP-compatible clients beyond Open WebUI.

