import subprocess
from utils.print_utils import print_agent

def bash_access(command: str):
    try:
        print_agent(f"About to run:\n{command}\nAllow? (y/n)")
        permission = input()

        if permission.strip().lower() in ["y","yes"]:
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