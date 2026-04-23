import json
import os
import sys
from pathlib import Path

import dct


def iter_fields_files(root_dir: Path):
    yield from root_dir.glob("nodes/**/fields.json")


def normalize_memory_name(memory_entry: dict[str, str]) -> str:
    return memory_entry["name"].split("/", 1)[-1]


def ensure_memory(memory_entry: dict[str, str]) -> None:
    memory_type = memory_entry["type"]
    memory_name = normalize_memory_name(memory_entry)
    location = memory_entry["ip/port"]
    memory = dct.get_memory_object(memory_name, location, memory_type)
    if memory is not None:
        return

    full_memory = {
        "name": memory_name,
        "ip/port": location,
        "type": memory_type,
        "group": [],
        "I": None,
        "eval": 0.0,
    }

    if memory_type == "redis":
        dct.set_redis_memory(location, memory_name, None, None, full_memory=full_memory)
        return

    if memory_type == "mongo":
        for field, value in full_memory.items():
            dct.set_mongo_memory(location, memory_entry["name"], field, value)
        return

    if memory_type in {"json", "local"}:
        memory_path = Path(location) / f"{memory_name}.json"
        memory_path.parent.mkdir(parents=True, exist_ok=True)
        memory_path.write_text(json.dumps(full_memory), encoding="utf-8")


def mount(codelets: list[str], root_dir: Path) -> None:
    fields_by_codelet: dict[str, Path] = {}
    for fields_path in iter_fields_files(root_dir):
        fields = json.loads(fields_path.read_text(encoding="utf-8"))
        fields_by_codelet[fields["name"]] = fields_path

    for codelet in codelets:
        fields_path = fields_by_codelet.get(codelet)
        if fields_path is None:
            raise FileNotFoundError(f"Unable to find fields.json for codelet {codelet!r}")

        fields = json.loads(fields_path.read_text(encoding="utf-8"))
        for memory_entry in fields.get("inputs", []):
            ensure_memory(memory_entry)


def main() -> None:
    root_dir = Path(os.getenv("DCT_EXAMPLES_ROOT", Path(__file__).resolve().parents[2]))
    mount(sys.argv[1:], root_dir)


if __name__ == "__main__":
    main()
