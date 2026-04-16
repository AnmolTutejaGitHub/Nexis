import os

def list_files(path):
    try:
        items = os.listdir(path)

        result = []
        for name in items:
            full_path = os.path.join(path,name)

            result.append({
                "name": name,
                "type": "dir" if os.path.isdir(full_path) else "file"
            })

        return {
            "success": True,
            "items": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }