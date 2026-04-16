import os
import shutil

def delete_path(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

        return {
            "success": True,
            "message": f"Deleted {path}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }