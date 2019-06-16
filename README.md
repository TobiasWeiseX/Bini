bini
=======================

This library gives you a bunch of functions to read, write and manipulate binary ini-files
used in windows programms like the game Freelancer.


```python
from bini import *

def negateEmpathy(b):
    version, sections = b
    for section in sections:
        secname, entries = section
        for entry in entries:
            entryname, values = entry
            if entryname == "empathy_rate":
                values[1] *= -1
    return b

if __name__ == "__main__":
    b = readBini("empathy.ini")
    writeIni("empathy.ini.txt", b)
    writeBini("empathy2.ini", negateEmpathy(b))
    print(biniToStr(b))
```