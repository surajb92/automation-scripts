import os
import sys
import re
import shutil

folpath = ""
if len(sys.argv) > 1:
    if not os.path.exists(sys.argv[1]):
        print("Invalid path given.")
        sys.exit(1)
    if sys.argv[1][0] == "~":
        folpath = os.path.join(os.path.expanduser("~"), sys.argv[1][1:])
    elif os.path.isabs(sys.argv[1]):
        folpath = sys.argv[1]
    else:
        folpath = os.path.abspath(sys.argv[1])
else:
    folpath = os.path.abspath(".")

print("Given path is : ", folpath)

dateformat = re.compile(
    r"""^(.*?)
    ((0|1)?\d)-
    ((0|1|2|3)?\d)-
    ((19|20)?\d{2})
    (.*?)$""",
    re.X,
)

for filename in os.listdir(folpath):
    mo = dateformat.search(filename)
    if not mo:
        continue
    before = mo.group(1)
    month = mo.group(2)
    date = mo.group(4)
    year = mo.group(6)
    after = mo.group(8)
    newname = before + date + "-" + month + "-" + year + after
    print("Renaming ", filename, " to ", newname, "\n")
    shutil.move(os.path.join(folpath, filename), os.path.join(folpath, newname))
