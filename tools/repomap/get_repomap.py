from tree_sitter import Language, Parser
from tree_sitter_languages import get_language
from tools.repomap.extension_map import EXTENSION_MAP
from tools.repomap.lang_node_map import LANG_NODE_MAP
import os


def detect_language(path):
    ext = os.path.splitext(path)[1].lower()
    return EXTENSION_MAP.get(ext)


def extract_nodes(node, node_types, extract_type, code_bytes, results=None):
    if results is None:
        results = []

    if node.type in node_types:
        if extract_type == "text":
            value = code_bytes[node.start_byte:node.end_byte].decode("utf-8")

        elif extract_type == "name":
            name_node = node.child_by_field_name("name")
            if name_node:
                value = code_bytes[name_node.start_byte:name_node.end_byte].decode("utf-8")
            else:
                value = "<anonymous>"

        results.append({
            "value": value,
            "start_line": node.start_point[0] + 1,
            "end_line": node.end_point[0] + 1,
        })

    for child in node.children:
        extract_nodes(child, node_types, extract_type, code_bytes, results)
    return results

def get_repomap(path):
    lang = detect_language(path)
    if not lang:
        return {"error": "Unsupported file type"}

    try:
        language = get_language(lang)
    except Exception as e:
        return {"error": f"Grammar not available for {lang}: {e}"}

    parser = Parser()
    parser.set_language(language)

    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    code_bytes = bytes(code, "utf-8")
    tree = parser.parse(code_bytes)
    root = tree.root_node

    if lang not in LANG_NODE_MAP:
        return {"error": f"No node map configured for '{lang}' — add it to lang_node_map.py"}
    node_map = LANG_NODE_MAP[lang]
    repomap = {}

    for category, config in node_map.items():
        node_types = set(config["types"])
        extract_type = config["extract"]
        found = extract_nodes(root, node_types, extract_type, code_bytes)
        if found:
            repomap[category] = found

    return {"language": lang, "file": path, "symbols": repomap}
