import os
import shutil
# from utils.human_feedback.ask_permission import ask_permission

def delete_path(path):
    try:
        # permission_granted = ask_permission(f"About to delete \n{path}\n Allow? y/n")
        # if not permission_granted:
        #      return f"Error: permission denied to delete {path}"

        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

        return f"Deleted {path}"

    except Exception as e:
        return f"Error: {str(e)[:500]}"