LANG_NODE_MAP = {
    "python": {
        "function": {
            "types": ["function_definition"],
            "extract": "name",
            "name_field": "name",
        },
        "class": {
            "types": ["class_definition"],
            "extract": "name",
            "name_field": "name",
        },
        "import": {
            "types": ["import_statement", "import_from_statement"],
            "extract": "text",
        },
    },
    "javascript": {
        "function": {
            "types": [
                "function_declaration",
                "generator_function_declaration",
                "method_definition",
                "arrow_function",
            ],
            "extract": "name",
            "name_field": "name",
        },
        "class": {
            "types": ["class_declaration"],
            "extract": "name",
            "name_field": "name",
        },
        "import": {
            "types": ["import_statement", "export_statement"],
            "extract": "text",
        },
    },
    "typescript": {
        "function": {
            "types": [
                "function_declaration",
                "generator_function_declaration",
                "method_definition",
                "arrow_function",
            ],
            "extract": "name",
            "name_field": "name",
        },
        "class": {
            "types": ["class_declaration"],
            "extract": "name",
            "name_field": "name",
        },
        "import": {
            "types": ["import_statement", "export_statement"],
            "extract": "text",
        },
    },
    "tsx": {
        "function": {
            "types": [
                "function_declaration",
                "generator_function_declaration",
                "method_definition",
                "arrow_function",
            ],
            "extract": "name",
            "name_field": "name",
        },
        "class": {
            "types": ["class_declaration"],
            "extract": "name",
            "name_field": "name",
        },
        "import": {
            "types": ["import_statement", "export_statement"],
            "extract": "text",
        },
    },
    "java": {
        "function": {
            "types": ["method_declaration", "constructor_declaration"],
            "extract": "name",
            "name_field": "name",
        },
        "class": {
            "types": ["class_declaration", "interface_declaration", "enum_declaration"],
            "extract": "name",
            "name_field": "name",
        },
        "import": {
            "types": ["import_declaration"],
            "extract": "text",
        },
    },
    "c": {
        "function": {
            "types": ["function_definition"],
            "extract": "name",
            "name_fields": ["declarator", "declarator"],
        },
        "class": {
            "types": ["struct_specifier"],
            "extract": "name",
            "name_field": "name",
        },
        "import": {
            "types": ["preproc_include"],
            "extract": "text",
        },
    },
    "cpp": {
        "function": {
            "types": ["function_definition"],
            "extract": "name",
            "name_fields": ["declarator", "declarator"],
        },
        "class": {
            "types": ["class_specifier", "struct_specifier"],
            "extract": "name",
            "name_field": "name",
        },
        "import": {
            "types": ["preproc_include"],
            "extract": "text",
        },
    },
    "go": {
        "function": {
            "types": ["function_declaration", "method_declaration"],
            "extract": "name",
            "name_field": "name",
        },
        "class": {
            "types": ["type_declaration"],
            "extract": "text",
        },
        "import": {
            "types": ["import_declaration"],
            "extract": "text",
        },
    },
    "rust": {
        "function": {
            "types": ["function_item"],
            "extract": "name",
            "name_field": "name",
        },
        "class": {
            "types": ["struct_item", "enum_item", "impl_item", "trait_item"],
            "extract": "name",
            "name_field": "name",
        },
        "import": {
            "types": ["use_declaration", "mod_item", "extern_crate_declaration"],
            "extract": "text",
        },
    },
    "ruby": {
        "function": {
            "types": ["method"],
            "extract": "name",
            "name_field": "name",
        },
        "class": {
            "types": ["class", "module"],
            "extract": "name",
            "name_field": "name",
        },
    },
    "php": {
        "function": {
            "types": ["function_definition"],
            "extract": "name",
            "name_field": "name",
        },
        "class": {
            "types": ["class_declaration"],
            "extract": "name",
            "name_field": "name",
        },
        "import": {
            "types": ["namespace_use_declaration"],
            "extract": "text",
        },
    },
    "kotlin": {
        "function": {
            "types": ["function_declaration"],
            "extract": "name",
            "name_field": "name",
        },
        "class": {
            "types": ["class_declaration", "object_declaration"],
            "extract": "name",
            "name_field": "name",
        },
    },
    "scala": {
        "function": {
            "types": ["function_definition"],
            "extract": "name",
            "name_field": "name",
        },
        "class": {
            "types": ["class_definition", "object_definition"],
            "extract": "name",
            "name_field": "name",
        },
        "import": {
            "types": ["import_declaration"],
            "extract": "text",
        },
    },
    "c_sharp": {
        "function": {
            "types": ["method_declaration", "constructor_declaration"],
            "extract": "name",
            "name_field": "name",
        },
        "class": {
            "types": ["class_declaration", "struct_declaration", "interface_declaration"],
            "extract": "name",
            "name_field": "name",
        },
        "import": {
            "types": ["using_directive"],
            "extract": "text",
        },
    },
    "bash": {
        "function": {
            "types": ["function_definition"],
            "extract": "name",
            "name_field": "name",
        },
    },
    "lua": {
        "function": {
            "types": ["function_declaration_statement"],
            "extract": "name",
            "name_field": "name",
        },
    },
    "r": {
        "function": {
            "types": ["function_definition"],
            "extract": "name",
            "name_field": "name",
        },
    },
    "perl": {
        "function": {
            "types": ["subroutine_declaration_statement", "function_definition"],
            "extract": "name",
            "name_field": "name",
        },
        "class": {
            "types": ["package_statement"],
            "extract": "text",
        },
        "import": {
            "types": ["use_no_statement"],
            "extract": "text",
        },
    },
    "haskell": {
        "function": {
            "types": ["function"],
            "extract": "name",
            "name_field": "name",
        },
        "class": {
            "types": ["data", "newtype", "type"],
            "extract": "text",
        },
        "import": {
            "types": ["import"],
            "extract": "text",
        },
    },
    "elixir": {},
    "sql": {
        "function": {
            "types": ["create_function_statement"],
            "extract": "name",
            "name_field": "name",
        },
    },
    "objc": {
        "function": {
            "types": ["method_definition", "method_declaration"],
            "extract": "name",
            "name_field": "name",
        },
        "class": {
            "types": ["class_interface", "class_implementation"],
            "extract": "name",
            "name_field": "name",
        },
        "import": {
            "types": ["preproc_import"],
            "extract": "text",
        },
    },
    "erlang": {
        "function": {
            "types": ["function_clause"],
            "extract": "name",
            "name_field": "name",
        },
        "class": {
            "types": ["module_attribute"],
            "extract": "name",
            "name_field": "name",
        },
    },
    "ocaml": {
        "function": {
            "types": ["value_definition"],
            "extract": "text",
        },
        "import": {
            "types": ["open_module"],
            "extract": "text",
        },
    },
    "fortran": {
        "function": {
            "types": ["subroutine_statement", "function_statement"],
            "extract": "name",
            "name_field": "name",
        },
    },
    "commonlisp": {
        "function": {
            "types": ["defun", "defmacro"],
            "extract": "name",
            "name_field": "name",
        },
    },
    "dockerfile": {
        "import": {
            "types": ["from_instruction"],
            "extract": "text",
        },
    },
    "gomod": {
        "import": {
            "types": ["module_directive"],
            "extract": "text",
        },
    },
    "html": {
        "class": {
            "types": ["element"],
            "extract": "text",
        },
    },
    "css": {
        "class": {
            "types": ["rule"],
            "extract": "text",
        },
    },
    "json": {
        "class": {
            "types": ["pair"],
            "extract": "text",
        },
    },
    "yaml": {
        "class": {
            "types": ["block_mapping_pair"],
            "extract": "text",
        },
    },
    "toml": {
        "class": {
            "types": ["pair", "table"],
            "extract": "text",
        },
    },
    "markdown": {
        "class": {
            "types": ["atx_heading", "setext_heading"],
            "extract": "text",
        },
    },
    "make": {
        "function": {
            "types": ["rule"],
            "extract": "text",
        },
    },
    "hcl": {
        "class": {
            "types": ["block"],
            "extract": "text",
        },
    },
    "regex": {
        "class": {
            "types": ["pattern"],
            "extract": "text",
        },
    },
}
