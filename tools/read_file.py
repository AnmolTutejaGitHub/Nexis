def read_file(path):
    try:
        with open(path,"r") as f:
            return {
                "success": True,
                "content": f.read()
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }