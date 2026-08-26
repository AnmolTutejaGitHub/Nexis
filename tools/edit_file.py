def edit_file(path: str, old_str: str = "", new_str: str = ""):
    try:
        with open(path, "r",encoding="utf-8") as f:
            original = f.read()

        if old_str == "":
            # accepted = preview_edit(path,original,new_str)

            # if not accepted:
                # return f"Error: file update rejected by user: {path}"

            with open(path, "w", encoding="utf-8") as f:
                f.write(new_str)

            return f"File updated: {path}"

        if old_str not in original:
            return (
                f"Error: old_str not found in {path}. "
                "Make sure to copy the exact text including whitespace/indentation. "
                "Read the target lines first if unsure."
            )

        count = original.count(old_str)
        if count > 1:
            lines = original.splitlines()
            match_line = next(
                i for i, l in enumerate(lines) if old_str.splitlines()[0] in l
            )
            context_start = max(0, match_line - 2)
            context_end = min(len(lines), match_line + len(old_str.splitlines()) + 2)
            context_snippet = "\n".join(lines[context_start:context_end])
            return (
                f"Error: old_str found {count} times in {path} — it must be unique. "
                "Expand old_str to include the surrounding lines shown below so it "
                f"matches exactly one location:\n\n{context_snippet}"
            )

        # accepted = preview_edit(path, old_str, new_str)

        # if not accepted:
        #     return f"Error: edit rejected by user: {path}"

        updated = original.replace(old_str, new_str, 1)

        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)

        # old_preview = "\n".join(f"- {l}" for l in old_str.splitlines())
        # new_preview = "\n".join(f"+ {l}" for l in new_str.splitlines())

        # return f"File edited: {path}\n{old_preview}\n{new_preview}"

        return f"File edited: {path}"

    except FileNotFoundError:
        return f"Error: file not found: {path}"
    except Exception as e:
        return f"Error: {str(e)[:500]}"
