from __future__ import annotations

from pathlib import Path

import dct
from dct.codelets import PythonCodelet


class SensorCodelet(PythonCodelet):
    def proc(self, activation: float) -> None:
        sensor_memory = dct.get_memory_objects_by_name(
            str(self.root_codelet_dir),
            "sensor",
            "outputs",
        )
        current_step = 0
        if sensor_memory:
            current_step = int(sensor_memory[0].get("step", 0))

        next_step = current_step + 1
        payload = f"reading-{next_step}"

        dct.set_memory_objects_by_name(
            str(self.root_codelet_dir),
            "sensor",
            "step",
            next_step,
            "outputs",
        )
        dct.set_memory_objects_by_name(
            str(self.root_codelet_dir),
            "sensor",
            "value",
            payload,
            "outputs",
        )


class WorkspaceCodelet(PythonCodelet):
    def proc(self, activation: float) -> None:
        sensor_memory = dct.get_memory_objects_by_name(
            str(self.root_codelet_dir),
            "sensor",
            "inputs",
        )
        if not sensor_memory:
            return

        reading = sensor_memory[0]
        summary = f"{reading['value']} processed at step {reading['step']}"

        dct.set_memory_objects_by_name(
            str(self.root_codelet_dir),
            "workspace",
            "latest_sensor_value",
            reading["value"],
            "outputs",
        )
        dct.set_memory_objects_by_name(
            str(self.root_codelet_dir),
            "workspace",
            "summary",
            summary,
            "outputs",
        )


def main() -> None:
    base_dir = Path(__file__).resolve().parent / "runtime"
    mind = dct.Mind(base_dir=base_dir)

    mind.add_memory("sensor", "json", initial_value={"step": 0, "value": None})
    mind.add_memory("workspace", "json", initial_value={"latest_sensor_value": None, "summary": None})

    mind.add_codelet(SensorCodelet, name="sensor", outputs=["sensor"], timestep=0)
    mind.add_codelet(WorkspaceCodelet, name="workspace", inputs=["sensor"], outputs=["workspace"], timestep=0)

    mind.run(steps=3)

    sensor_memory = dct.get_local_memory(str(base_dir / "memories"), "sensor")
    workspace_memory = dct.get_local_memory(str(base_dir / "memories"), "workspace")

    print("sensor =", sensor_memory)
    print("workspace =", workspace_memory)


if __name__ == "__main__":
    main()
