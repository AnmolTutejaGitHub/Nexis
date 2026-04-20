from utils.human_feedback.preview_edit import preview_edit

def edit_file(path: str, old_str: str, new_str: str):
    try:
        with open(path, "r",encoding="utf-8") as f:
            original = f.read()

        if old_str not in original:
            return {
                "success": False,
                "error": (
                    "old_str not found in file. "
                    "Make sure to copy the exact text including whitespace/indentation. "
                    "Call read_file first if unsure."
                )
            }

        count = original.count(old_str)
        if count > 1:
            return {
                "success": False,
                "error": (
                    f"old_str found {count} times in the file — it must be unique. "
                    "Add more surrounding lines to make it unambiguous."
                )
            }

        accepted = preview_edit(path, old_str, new_str)

        if not accepted:
            return {
                "success": False,
                "error": "Edit rejected by user."
            }

        updated = original.replace(old_str, new_str, 1)

        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)

        old_preview = "\n".join(f"- {l}" for l in old_str.splitlines())
        new_preview = "\n".join(f"+ {l}" for l in new_str.splitlines())

        return {
            "success": True,
            "message": f"File edited: {path}",
            "diff_preview": f"{old_preview}\n{new_preview}"
        }

    except FileNotFoundError:
        return {"success": False, "error": f"File not found: {path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
