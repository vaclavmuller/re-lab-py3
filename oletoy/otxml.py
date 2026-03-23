# Copyright (C) 2007-2013   Valek Filippov (frob@df.ru)

import sys, struct, gtk
from utils import *

def open(buf, page, parent):
    print("Probably XML", page.model.get_value(parent,0))
    if isinstance(buf, (bytes, bytearray)):
        if buf[0:2] == b'\xff\xfe':
            buf = buf[2:].decode('utf_16le', errors='replace')
        elif buf[0:2] == b'\xfe\xff':
            buf = buf[2:].decode('utf_16be', errors='replace')
        else:
            buf = buf.decode('utf-8', errors='replace')
    t = buf.split("<")
    piter = parent
    citer = []

    for i in range(len(t)-1):
        foo = t[i+1].split()
        if len(foo) > 0:
            bar = foo[0]
        else:
            bar = foo[:-1]

        if not bar:
            continue
        if bar[0] == "?":
            id = bar[1:]
        else:
            id = bar

        if id and id[0] == "/":
            if citer:
                piter = citer.pop()
        else:
            niter = add_pgiter(page, id, "otxml", 0, len(t[i+1]), t[i+1], piter)
            citer.append(piter)
            piter = niter
