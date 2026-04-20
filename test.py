import tempfile, os
from tools.edit_file import edit_file
from utils.print_utils import print_tool_result
from tools.ask_human import ask_human

DUMMY = os.path.join(tempfile.gettempdir(), "nexis_test_edit.py")

ORIGINAL = """\
def greet(name):
    print("Hello " + name)

def add(a, b):
    return a + b
"""

with open(DUMMY, "w") as f:
    f.write(ORIGINAL)

print(f"Test file created at: {DUMMY}\n")

result = edit_file(
    path=DUMMY,
    old_str='def greet(name):\n    print("Hello " + name)',
    new_str='def greet(name):\n    """Say hello."""\n    print(f"Hello, {name}!")',
)

print_tool_result(result)

ask_human("should I delete the os to get rid of all problems ?")