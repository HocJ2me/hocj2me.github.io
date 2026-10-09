# -*- coding: utf-8 -*-
"""Tô màu cú pháp đơn giản cho C++, Python, Java (sinh sẵn HTML lúc build)."""
import re
from html import escape

KW = {
 "cpp": """alignas auto bool break case catch char class const constexpr const_cast continue decltype default delete do
  double dynamic_cast else enum explicit extern false final float for friend goto if inline int long mutable namespace
  new noexcept nullptr operator override private protected public return short signed sizeof static static_cast struct
  switch template this throw true try typedef typename union unsigned using virtual void volatile while size_t""",
 "py": """False None True and as assert async await break class continue def del elif else except finally for from
  global if import in is lambda nonlocal not or pass raise return try while with yield match case self cls""",
 "java": """abstract boolean break byte case catch char class continue default do double else enum extends final finally
  float for if implements import instanceof int interface long new null package private protected public record return
  short static super switch synchronized this throw throws true false try void volatile while var""",
}
KW = {k: set(v.split()) for k, v in KW.items()}

PATTERNS = {
 "cpp": [
   ("com", r"//[^\n]*|/\*.*?\*/"),
   ("pre", r"^[ \t]*#[a-z]+[^\n]*"),
   ("str", r'"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])\''),
 ],
 "py": [
   ("str", r'[rbfuRBFU]{0,2}(?:"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\')'),
   ("com", r"#[^\n]*"),
   ("ann", r"@[A-Za-z_][\w.]*"),
 ],
 "java": [
   ("com", r"//[^\n]*|/\*.*?\*/"),
   ("str", r'"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])\''),
   ("ann", r"@[A-Za-z_]\w*"),
 ],
}
COMMON = [
  ("num", r"\b(?:0x[0-9A-Fa-f]+|\d[\d_']*(?:\.\d+)?[fFLu]*)\b"),
  ("id", r"[A-Za-z_]\w*"),
]


def highlight(code, lang):
    parts = PATTERNS[lang] + COMMON
    rx = re.compile("|".join(f"(?P<{n}>{p})" for n, p in parts), re.S | re.M)
    kws = KW[lang]
    out, pos = [], 0
    for m in rx.finditer(code):
        out.append(escape(code[pos:m.start()]))
        kind, text = m.lastgroup, m.group()
        if kind == "id":
            nxt = code[m.end():m.end() + 1]
            if text in kws:
                kind = "kw"
            elif text[0].isupper():
                kind = "ty"
            elif nxt == "(":
                kind = "fn"
            else:
                out.append(escape(text)); pos = m.end(); continue
        out.append(f'<span class="t-{kind}">{escape(text)}</span>')
        pos = m.end()
    out.append(escape(code[pos:]))
    return "".join(out)
