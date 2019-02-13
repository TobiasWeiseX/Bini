#!/usr/bin/env python3
"""
A lib to parse and modify bini-files

------------------------------------
The parsed bini is a tuple:

bini = (int,[section])
section = (str,[entry])
entry = (str,[value])
value = int | float | string
------------------------------------

Example:

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

"""
from functools import reduce as _reduce
from struct import pack as _pack
from struct import unpack as _unpack

def _nub(ls):
    rs = []
    for x in ls:
        if not x in rs:
            rs.append(x)
    return rs

def _concat(iterable):
    return _reduce(lambda a,b: a+b,iterable)


#========= IO ============

def _readBinFile(p):
    with open(p,"rb") as f:
        return f.read()

def _writeFile(p,c):
    with open(p,"w") as f:
        f.write(c)

def _writeBinFile(p,c):
    with open(p,"wb") as f:
        f.write(c)

def _getOffset(table, offset):
    r = ""
    for c in table[offset:]:
        if c==0: break
        r += chr(c)
    return r

def _parseVal(f,strtable):
    typ, bstr = _unpack("<B", f.read(1))[0], f.read(4)
    if typ == 1: return _unpack("<i", bstr)[0]
    elif typ == 2: return _unpack("<f", bstr)[0]
    elif typ == 3: return _getOffset(strtable, _unpack("<i", bstr)[0])
    raise Exception("Unknown bini-type!("+str(typ)+")")

def _parseEntry(f, strtable):
    offset, num = _unpack("<HB", f.read(3))
    return _getOffset(strtable,offset), [_parseVal(f,strtable) for i in range(num)]

def _parseSection(f, table):
    offset, n = _unpack("<HH", f.read(4))
    return _getOffset(table,offset), [_parseEntry(f,table) for i in range(n)]


def _while(f):
    i = 0
    while f():
        yield i
        i += 1

def readBini(path):
    """
    read a bini-file and parse it into its abstract representation
    """
    with open(path,"rb") as f:
        if f.read(4)!=b"BINI": raise Exception("Not a bini-file!")
        version, offset = _unpack("<ii", f.read(8))
        table = _readBinFile(path)[offset:]
        return version, [_parseSection(f,table) for i in _while(lambda: offset > f.tell()) ]


def _entry2str(entry):
    name, vals = entry
    return name+" = "+", ".join(map(str,vals))


def biniToStr(bini):
    """
    creates a string from the bini-representation
    """
    return _concat(("["+secname+"]\n"+"\n".join(map(_entry2str,entries))+"\n\n" for secname, entries in bini[1]))

#============= Building the bini-bstr ================

def _createDict(strs):
    d = {}
    offset = 0
    for s in strs:
        d[s] = offset
        offset += len(s)+1
    return d

def _str2bstr(s):
    return bytes(s,"ascii")

def _section2bstr(d, section):
    secname, entries = section
    return _pack("<HH", d[secname], len(entries)) + b"".join((_entry2bstr(d,e) for e in entries))

def _entry2bstr(d, entry):
    name, vals = entry
    return _pack("<HB", d[name], len(vals)) + b"".join((_val2bstr(d,v) for v in vals))


def _val2bstr(d, v):
    t = type(v)
    if t == int: return _pack("<Bi", 1, v)
    elif t == float: return _pack("<Bf", 2, v)
    elif t == str: return _pack("<Bi", 3, d[v])

def _unzip(ls):
    return ([a for a,b in ls],[b for a,b in ls])

def _bini2strs(bini):
    secs = bini[1]
    secnames, es = _unzip(secs)
    entries = _concat(es)
    entrynames = [ n for n, vals in entries ]
    values = [x for x in _concat([vals for n, vals in entries]) if type(x)==str]
    return _nub(secnames + entrynames + values)


def _bini2bstr(bini):
    version, sections = bini
    strs = _bini2strs(bini)
    d = _createDict(strs)
    body = _concat([_section2bstr(d, sec) for sec in sections])
    return b"BINI" + _pack("<ii",version, 12+len(body)) + body + b"\x00".join(map(_str2bstr,strs))

#=================== public =================================

def writeBini(path, bini):
    """
    create a bini-file using its abstract representation
    """
    _writeBinFile(path, _bini2bstr(bini))

def writeIni(path, bini):
    """
    create an ini-file using the bini's abstract representation
    """
    _writeFile(path, biniToStr(bini))







