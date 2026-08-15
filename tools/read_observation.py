import json
from utils.observations import read_observation as read_saved_observation

def read_observation(observation_id):
    saved = read_saved_observation(observation_id)

    if not saved.get("success"):
        return f"Error: {saved.get('error', 'observation not found')}"

    observation = saved.get("observation", {})
    result = observation.get("result", "")

    if isinstance(result, str):
        return result

    return json.dumps(result, ensure_ascii=False, default=str)
