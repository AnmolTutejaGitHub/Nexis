import json
import os
from uuid import uuid4

OBS_DIR = ".nexis/observations"

def new_observation_id():
    return uuid4().hex[:8]

def create_observation(tool_name, result):
    try:
        os.makedirs(OBS_DIR, exist_ok=True)

        obs_id = new_observation_id()
        path = os.path.join(OBS_DIR, f"{obs_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({
                "id": obs_id,
                "tool": tool_name,
                "result": result,
            }, f, ensure_ascii=False)
        return obs_id
    except Exception as e:
        return "error:" + str(e)

def read_observation(obs_id):
    path = os.path.join(OBS_DIR, f"{obs_id}.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return {
                "success": True,
                "observation_id": obs_id,
                "observation": json.load(f),
            }
    except FileNotFoundError:
        return {
            "success": False,
            "error": f"Observation not found: {obs_id}",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
