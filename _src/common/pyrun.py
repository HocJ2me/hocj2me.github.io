# -*- coding: utf-8 -*-
"""Chạy một script Python cho bài học: in lại dữ liệu nhập (như người dùng vừa gõ) và rút gọn traceback.
Dùng: python -u -I pyrun.py <file.py> [1=echo input]"""
import builtins, os, sys, traceback

path = sys.argv[1]
name = os.path.basename(path)
if len(sys.argv) > 2 and sys.argv[2] == "1":
    _input = builtins.input

    def input_echo(prompt=""):
        v = _input(prompt)
        print(v)
        return v
    builtins.input = input_echo

sys.argv = [name]
src = open(path, encoding="utf-8").read()
try:
    exec(compile(src, name, "exec"), {"__name__": "__main__", "__file__": name})
except SystemExit:
    raise
except BaseException as e:
    sys.stdout.flush()
    traceback.print_exception(type(e), e, e.__traceback__.tb_next)
    sys.exit(1)
