import subprocess
from utils.print_utils import print_agent
from utils.human_feedback.ask_permission import ask_permission

def bash_access(command: str):
    try:
        permission_granted = ask_permission(f"About to run:\n{command}\nAllow? (y/n)")

        if permission_granted:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        
        return {
            "error" : f"Permission denied to run command {command}"
        }

    except Exception as e:
        return {"error": str(e)}