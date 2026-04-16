import os

def update_file(path, content):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "success": True,
            "message": f"File updated: {path}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }