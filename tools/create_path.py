import os

def create_path(path, type="file", content=""):
    try:
        if type == "folder":
            os.makedirs(path,exist_ok=True)
        else:
            with open(path, "w") as f:
                f.write(content)

        return {
            "success": True,
            "message": f"{type} created at {path}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }