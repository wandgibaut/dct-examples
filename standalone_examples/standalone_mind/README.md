# Standalone Mind Example

This example runs DCT as a single local Python application with `dct.Mind`.
It does not start nodes, servers, Docker containers, Redis, or MongoDB.

## Requirements

Install the package in the Python environment you want to use:

```bash
python -m pip install dct-python
```

## Run

From this directory:

```bash
python app.py
```

The script will:

1. Create a local standalone mind under `./runtime`.
2. Create two JSON memories: `sensor` and `workspace`.
3. Run two codelets in-process for three deterministic steps.
4. Print the final contents of both memories.

You can inspect the generated files under `runtime/codelets` and `runtime/memories`.
