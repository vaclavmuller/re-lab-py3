# re-lab (oletoy + colupatr) – Python 3 port (Windows)

> Python 3 + GTK3 port of the original re-lab tools, focused on restoring functionality on modern Windows systems.

This repository contains a Python 3 port of the original re-lab project:
- oletoy
- colupatr

## Origin

Original project:
https://github.com/renyxa/re-lab

This repository is an **unofficial continuation / port** of the original project.

This port was created to make the tools usable again on modern systems:
- Python 3.14
- Windows
- GTK3 (gvsbuild)

## Status

- Application startup: OK
- GUI: OK
- Hex view (selection, scroll, redraw): OK
- File open (including Unicode paths): OK
- YEP parser: working (structure + detail view)
- Graph / Diff view: working

Some parsers are still incomplete or not fully ported:
- qxp (import issues)
- publisher1 (syntax issues)

## Notes

This is a conservative port:
- goal was to preserve original functionality
- minimal invasive changes
- compatibility layer added (gtk_compat.py)

## Running (Windows)

Requires:
- Python 3.14
- GTK runtime (gvsbuild)
- virtual environment (venv314)

Run using:
start_oletoy.bat
start_colupatr.bat


## Author of this port

Václav Müller

---

Original authors:
see AUTHORS files in the project
