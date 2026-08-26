import subprocess
# from utils.human_feedback.ask_permission import ask_permission

def bash_access(command: str):
    try:
        # permission_granted = ask_permission(f"About to run:\n{command}\nAllow? (y/n)")

        # if permission_granted:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        parts = []
        if result.stdout:
            parts.append(result.stdout.rstrip())
        if result.stderr:
            parts.append(f"stderr: {result.stderr.rstrip()}")
        if result.returncode:
            parts.append(f"exit {result.returncode}")

        return "\n".join(parts) or "(no output)"

        #return f"Error: permission denied to run command {command}"

    except Exception as e:
        return f"Error: {str(e)[:500]}"