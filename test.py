import tempfile, os
from tools.edit_file import edit_file
from utils.print_utils import print_tool_result
from tools.ask_human import ask_human


def main():
    dummy = os.path.join(tempfile.gettempdir(), "nexis_test_edit.py")

    original = """\
def greet(name):
    print("Hello " + name)

def add(a, b):
    return a + b
"""

    with open(dummy, "w") as f:
        f.write(original)

    print(f"Test file created at: {dummy}\n")

    result = edit_file(
        path=dummy,
        old_str='def greet(name):\n    print("Hello " + name)',
        new_str='def greet(name):\n    """Say hello."""\n    print(f"Hello, {name}!")',
    )

    print_tool_result(result)

    ask_human("should I delete the os to get rid of all problems ?")


if __name__ == "__main__":
    main()
