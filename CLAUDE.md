## Rules
- ALWAYS use `uv` as the Python interface. NEVER use the `python` command directly
- `uv` is reponsible of handling requirements. DO NOT rely on anything else other than `uv`
- ALWAYS use `docker` for executing `uv` and database commands, migrations, etc. ALL development MUST be done through `docker` to avoid polluting the local environment
- Use `docker ...` commands as needed
