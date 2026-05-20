from utils.human_feedback.preview_edit import preview_edit

def edit_file(path: str, old_str: str = "", new_str: str = ""):
    try:
        with open(path, "r",encoding="utf-8") as f:
            original = f.read()

        if old_str == "":
            accepted = preview_edit(path,original,new_str)

            if not accepted:
                return {
                    "success": False,
                    "path": path,
                    "error": "File update rejected by user."
                }

            with open(path, "w", encoding="utf-8") as f:
                f.write(new_str)

            return {
                "success": True,
                "path": path,
                "message": f"File updated: {path}"
            }

        if old_str not in original:
            return {
                "success": False,
                "path" : path,
                "error": (
                    "old_str not found in file. "
                    "Make sure to copy the exact text including whitespace/indentation. "
                    "Call read_file first if unsure."
                )
            }

        count = original.count(old_str)
        if count > 1:
            lines = original.splitlines()
            match_line = next(
                i for i, l in enumerate(lines) if old_str.splitlines()[0] in l
            )
            context_start = max(0, match_line - 2)
            context_end = min(len(lines), match_line + len(old_str.splitlines()) + 2)
            context_snippet = "\n".join(lines[context_start:context_end])
            return {
                "success": False,
                "path": path,
                "error": (
                    f"old_str found {count} times in the file — it must be unique. "
                    "Expand old_str to include the surrounding lines shown below so it matches exactly one location:\n\n"
                    f"{context_snippet}"
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
            "path": path,
            "message": f"File edited: {path}",
            "diff_preview": f"{old_preview}\n{new_preview}"
        }

    except FileNotFoundError:
        return {"success": False, "error": f"File not found: {path}"}
    except Exception as e:
        return {"success": False, "error": str(e)[:500]}
