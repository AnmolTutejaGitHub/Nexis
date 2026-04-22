def read_file(path):
    try:
        with open(path,"r") as f:
            return {
                "success": True,
                "path": path,
                "content": f.read()
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def read_file_range(path,start_line,end_line):
    try:
        with open(path,"r") as f:
            lines = f.readlines()

        start = max(0, start_line - 1)
        end = min(len(lines), end_line)
        return {
            "success": True,
             "path": path,
            "start_line": start_line,
            "end_line": end_line,
            "content": "".join(lines[start:end])
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }