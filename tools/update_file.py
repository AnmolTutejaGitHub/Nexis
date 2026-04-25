import os
from utils.human_feedback.preview_edit import preview_edit

def update_file(path, content):
    try:
        if os.path.exists(path):
            with open(path,"r",encoding="utf-8") as f:
                old_content = f.read()
        else:
            old_content = ""

        accepted = preview_edit(path,old_content,content)

        if not accepted:
            return {
                "success": False,
                "path": path,
                "error": "File update rejected by user."
            }

        with open(path,"w",encoding="utf-8") as f:
            f.write(content)

        return {
            "success": True,
            "path": path,
            "message": f"File updated: {path}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }