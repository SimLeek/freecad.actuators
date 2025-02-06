#!/usr/bin/env python3

#crappy chatgpt code, but it works

import re
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))

def process_file(filepath):
    # Read the original file
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    # Flag to know if we already inserted the os block
    inserted_os_block = False

    # --- First, remove any 'import img_src_rc' lines ---
    lines = [line for line in lines if "import img_src_rc" not in line]

    # --- Process import block replacement ---
    # We will look for three consecutive lines that import from PySide2/Pyside2
    # for QtCore, QtGui, and QtWidgets. We use a sliding window.
    i = 0
    replaced_import_block = False
    while i < len(lines):
        # Try to match the three lines starting at index i.
        if (i + 2 < len(lines) and
            re.match(r'^\s*from\s+Pyside2\.QtCore\s+import\s+\*\s*(#.*)?$', lines[i], re.IGNORECASE) and
            re.match(r'^\s*from\s+Pyside2\.QtGui\s+import\s+\*\s*(#.*)?$', lines[i+1], re.IGNORECASE) and
            re.match(r'^\s*from\s+Pyside2\.QtWidgets\s+import\s+\*\s*(#.*)?$', lines[i+2], re.IGNORECASE)):
            # Replace these three lines with a try/except block.
            new_lines.append("try:\n")
            new_lines.append("    from PySide2.QtCore import *  # type: ignore\n")
            new_lines.append("    from PySide2.QtGui import *  # type: ignore\n")
            new_lines.append("    from PySide2.QtWidgets import *  # type: ignore\n")
            new_lines.append("except ImportError:\n")
            new_lines.append("    from PySide.QtCore import *  # type: ignore\n")
            new_lines.append("    from PySide.QtGui import *  # type: ignore\n")
            new_lines.append("    from PySide.QtWidgets import *  # type: ignore\n")
            i += 3
            replaced_import_block = True
            continue
        else:
            new_lines.append(lines[i])
            i += 1

    # If we did not find and replace the import block, then we might still have
    # one or more lines that start with "from PySide2" or "from Pyside2". In that case,
    # we can attempt a more general replacement.
    if not replaced_import_block:
        combined = "".join(new_lines)
        # This regex finds three separate import lines for QtCore, QtGui and QtWidgets.
        pattern = (r"(from\s+Pyside2\.QtCore\s+import\s+\*.*\n"
                   r"from\s+Pyside2\.QtGui\s+import\s+\*.*\n"
                   r"from\s+Pyside2\.QtWidgets\s+import\s+\*.*\n)")
        repl = ("try:\n"
                "    from PySide2.QtCore import *  # type: ignore\n"
                "    from PySide2.QtGui import *  # type: ignore\n"
                "    from PySide2.QtWidgets import *  # type: ignore\n"
                "except ImportError:\n"
                "    from PySide.QtCore import *  # type: ignore\n"
                "    from PySide.QtGui import *  # type: ignore\n"
                "    from PySide.QtWidgets import *  # type: ignore\n")
        combined_new = re.sub(pattern, repl, combined, flags=re.IGNORECASE)
        new_lines = combined_new.splitlines(keepends=True)

    # --- Insert os block after import section and before first class definition ---
    # We assume the "import section" is at the top.
    # Find the index of the first non-import line that is a class definition.
    insert_index = None
    for idx, line in enumerate(new_lines):
        # Skip blank lines and comments.
        if line.strip() == "" or line.strip().startswith("#"):
            continue
        # If this line starts with "class " then we insert the block above it.
        if re.match(r'^\s*class\s+', line):
            insert_index = idx
            break

    # If we found a location to insert and haven't inserted yet:
    if insert_index is not None:
        os_block = "import os \ndir_path = os.path.dirname(os.path.realpath(__file__))\n"
        # Insert os_block above the first class definition.
        new_lines.insert(insert_index, os_block)
    else:
        # If no class definition is found, append the os_block at the end of the imports.
        new_lines.append("\nimport os \ndir_path = os.path.dirname(os.path.realpath(__file__))\n")

    # --- Modify .svg occurrences inside setStyleSheet calls ---
    # Look for lines that mention .svg and setStyleSheet.
    pattern_svg = re.compile(r'url\(:/images/([^)\s]+\.svg)\)')
    for idx, line in enumerate(new_lines):
        if ".svg" in line and "setStyleSheet" in line:
            # Replace the url(...) part with the new format.
            new_line = pattern_svg.sub(r"url('{dir_path+os.sep}\1')", line)
            # Also, if the string literal starts with u" then replace with f"
            new_line = re.sub(r'(setStyleSheet\()\s*u"', r'\1f"', new_line)
            new_lines[idx] = new_line

    # Write back to the file
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def main():
    try:
        if len(sys.argv) != 2:
            #print("Usage: python fix_ui.py <path_to_python_file>")
            #sys.exit(1)
            filepath = dir_path+os.sep+"planetary_ui.py"
        else:
            filepath = sys.argv[1]
            if not os.path.isfile(filepath):
                print(f"Error: File '{filepath}' does not exist.")
                sys.exit(1)

        process_file(filepath)
        print(f"File '{filepath}' has been successfully modified.")
    except Exception as e:
        print("An error occurred while processing the file:")
        print(e)

if __name__ == '__main__':
    main()
