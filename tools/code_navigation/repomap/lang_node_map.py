LANG_NODE_MAP = {
    "python": {
        "function": {
            "types": ["function_definition"],
            "extract": "name"
        },
        "class": {
            "types": ["class_definition"],
            "extract": "name"
        },
        "import": {
            "types": ["import_statement", "import_from_statement"],
            "extract": "text"
        }
    },
    "javascript": {
        "function": {
            "types": [
                "function_declaration",
                "generator_function_declaration",
                "method_definition",
            ],
            "extract": "name"
        },
        "class": {
            "types": ["class_declaration"],
            "extract": "name"
        },
        "import": {
            "types": ["import_statement"],
            "extract": "text"
        }
    },
}