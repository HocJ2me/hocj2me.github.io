# -*- coding: utf-8 -*-
"""Bộ sinh trang khóa học dùng chung (C++ cơ bản, FreeRTOS, PCB...).

Một khóa khai báo dict COURSE (xem _src/cpp-co-ban/course.py) gồm:
  slug, title, short_title, icon, sub, gradient (2-3 màu), storage (tiền tố localStorage),
  overview (HTML trang tổng quan), groups: [(key, tên nhóm, mô tả, [lesson...])]
  code_dir, runner: hàm (đường_dẫn_file, stdin) -> (lệnh hiển thị, output)  (None nếu khóa không có code)

Mỗi lesson là dict:
  id, title, icon, goal (1 câu), goals [...], intro (HTML),
  sections: [dict(h, html, fig, figcap, code, stdin, notes, solution)],
  embedded [...], mistakes [...], summary [...], exercises [...], refs [(text, url)]
"""
import hashlib, json, os, subprocess, sys, tempfile
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from highlight import highlight

GROUP_COLORS = ["#0891b2", "#d97706", "#7c3aed", "#16a34a", "#db2777", "#2563eb"]


# ------------------------------------------------------------------ chạy code (có cache)
class Runner:
    def __init__(self, cache_file):
        self.cache_file = cache_file
        self.cache = json.load(open(cache_file, encoding="utf-8")) if os.path.exists(cache_file) else {}

    def _save(self):
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        json.dump(self.cache, open(self.cache_file, "w", encoding="utf-8"), ensure_ascii=False, indent=0)

    def run(self, key_parts, fn):
        h = hashlib.sha1()
        for p in key_parts:
            h.update(p if isinstance(p, bytes) else str(p).encode("utf-8"))
        key = h.hexdigest()
        if key not in self.cache:
            self.cache[key] = fn()
            self._save()
        return self.cache[key]


def run_cpp(path, stdin=None, sources=(), flags=(), include=(), runner=None, timeout=60):
    """Biên dịch 1 file C++ (kèm sources phụ) bằng g++ và chạy, trả về output (stdout+stderr)."""
    def go():
        tmp = tempfile.mkdtemp()
        exe = os.path.join(tmp, "a.exe")
        cmd = ["g++", "-std=c++17", "-O1", "-Wall", "-Wextra", *flags, *[f"-I{i}" for i in include], path, *sources, "-o", exe, "-static"]
        c = subprocess.run(cmd, capture_output=True)
        if c.returncode:
            sys.exit(f"Lỗi biên dịch {path}:\n{c.stderr.decode('utf-8', 'replace')[-3000:]}")
        r = subprocess.run([exe], input=(stdin or "").encode("utf-8"), stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, cwd=tmp, timeout=timeout)
        out = r.stdout.decode("utf-8", "replace").replace("\r\n", "\n").rstrip()
        print("  chạy", os.path.basename(path))
        return out
    parts = [open(path, "rb").read(), stdin or "", *flags, *[open(s, "rb").read() for s in sources if s.endswith((".c", ".cpp", ".h"))]]
    return runner.run(parts, go)


# ------------------------------------------------------------------ render
def li(items):
    return "".join(f"<li>{x}</li>" for x in items)


def code_block(fname, code, run_cmd, output, stdin=None, lang="cpp", solution=False):
    lines = code.count("\n")
    box = f'''<div class="codebox">
    <div class="codebar"><span class="fname">{escape(fname)}</span><span class="lines">{lines} dòng</span>
      <button class="cbtn" data-act="copy">Sao chép</button><button class="cbtn" data-act="dl" data-name="{escape(fname)}">Tải file</button></div>
    <pre class="code"><code>{highlight(code, lang)}</code></pre>
  </div>'''
    extra = ""
    if run_cmd:
        extra += f'<div class="runcmd"><span>▶ Chạy thử:</span> <code>{escape(run_cmd)}</code></div>'
    if stdin:
        extra += f'<div class="outbox inbox"><div class="outbar">Dữ liệu nhập từ bàn phím</div><pre class="out">{escape(stdin.rstrip())}</pre></div>'
    if output is not None:
        extra += f'<div class="outbox"><div class="outbar">Kết quả khi chạy (đã chạy thật lúc soạn bài)</div><pre class="out">{escape(output)}</pre></div>'
    body = box + extra
    if solution:
        return f'<details class="sol"><summary>Xem lời giải</summary>{body}</details>'
    return body


def render_lesson(C, L, idx, total, gkey, gname, gcolor, prev, nxt):
    secs = []
    for i, s in enumerate(L.get("sections", []), 1):
        parts = [f'<h3 id="{L["id"]}-s{i}"><span class="n">{i}</span>{s["h"]}</h3>']
        if s.get("html"):
            parts.append(f'<div class="prose">{s["html"]}</div>')
        if s.get("fig"):
            cap = f'<figcaption>{s["figcap"]}</figcaption>' if s.get("figcap") else ""
            parts.append(f'<figure class="fig">{s["fig"]}{cap}</figure>')
        if s.get("code"):
            path = os.path.join(C["code_dir"], s["code"])
            code = open(path, encoding="utf-8").read().rstrip() + "\n"
            cmd, out = C["runner"](path, s.get("stdin")) if C.get("runner") else (None, None)
            parts.append(code_block(s["code"], code, cmd, out, s.get("stdin"), C.get("lang", "cpp"), s.get("solution")))
        if s.get("notes"):
            parts.append(f'<h4 class="sub">Giải thích</h4><ul class="notes">{li(s["notes"])}</ul>')
        if s.get("after"):
            parts.append(f'<div class="prose">{s["after"]}</div>')
        secs.append("\n".join(parts))
    blocks = []
    if L.get("embedded"):
        blocks.append(f'<h3><span class="n">🔧</span>Áp dụng trong lập trình nhúng</h3><div class="emb"><div class="embicon">🔧</div><ul>{li(L["embedded"])}</ul></div>')
    if L.get("mistakes"):
        blocks.append(f'<h3><span class="n">⚠</span>Lỗi thường gặp</h3><div class="mist"><ul>{li(L["mistakes"])}</ul></div>')
    if L.get("summary"):
        blocks.append(f'<h3><span class="n">✓</span>Tóm tắt</h3><ul class="summary">{li(L["summary"])}</ul>')
    if L.get("exercises"):
        ex = "".join(f'<li><label><input type="checkbox" data-ex="{L["id"]}-{k}"> <span>{e}</span></label></li>' for k, e in enumerate(L["exercises"]))
        blocks.append(f'<h3><span class="n">✎</span>Bài tập về nhà</h3><ol class="ex">{ex}</ol>')
    refs = ""
    if L.get("refs"):
        refs = '<div class="refs">📚 Đọc thêm: ' + " · ".join(f'<a href="{u}" target="_blank" rel="noopener">{escape(t)}</a>' for t, u in L["refs"]) + "</div>"
    goals = f'<div class="goals"><b>Sau bài này bạn sẽ:</b><ul>{li(L["goals"])}</ul></div>' if L.get("goals") else ""
    nav_prev = f'<a class="pn" href="#{prev[0]}">← {escape(prev[1])}</a>' if prev else "<span></span>"
    nav_next = f'<a class="pn next" href="#{nxt[0]}">{escape(nxt[1])} →</a>' if nxt else "<span></span>"
    return f'''
<section class="lesson" id="{L["id"]}" data-title="{escape(L["title"])}" hidden>
  <div class="hero" style="--g:{gcolor}">
    <div class="crumbs"><span class="gchip">{escape(gname)}</span><span>Bài {idx}/{total}</span>{('<span>⏱ ' + L["time"] + '</span>') if L.get("time") else ""}</div>
    <h2><span class="hicon">{L.get("icon", "")}</span> {escape(L["title"])}</h2>
    <p class="intent">{L.get("goal", "")}</p>
  </div>
  {goals}
  {('<div class="prose lead">' + L["intro"] + '</div>') if L.get("intro") else ""}
  {"".join(secs)}
  {"".join(blocks)}
  {refs}
  <div class="donebar"><button class="donebtn" data-done="{L["id"]}">☐ Đánh dấu đã học xong bài này</button></div>
  <nav class="pnav">{nav_prev}{nav_next}</nav>
</section>'''


def build(C, out_path):
    lessons_all = [L for _, _, _, ls in C["groups"] for L in ls]
    order = [("overview", "Tổng quan")] + [(L["id"], L["title"]) for L in lessons_all]
    html_lessons = [f'''
<section class="lesson" id="overview" data-title="Tổng quan" hidden>
  <div class="hero" style="--g:{C["gradient"][0]}">
    <div class="crumbs"><span class="gchip">Bài mở đầu</span><span>{escape(C["badge"])}</span></div>
    <h2>{C["icon"]} {escape(C["title"])}</h2>
    <p class="intent">{C["tagline"]}</p>
    <div class="ovstats">{"".join(f"<div><b>{v}</b><span>{escape(k)}</span></div>" for k, v in C["stats"])}<div><b id="ovDone">0</b><span>bài đã học</span></div></div>
    <a class="startbtn" href="#{lessons_all[0]["id"]}">Bắt đầu bài 1 →</a>
  </div>
  {C["overview"]}
  <nav class="pnav"><span></span><a class="pn next" href="#{lessons_all[0]["id"]}">{escape(lessons_all[0]["title"])} →</a></nav>
</section>''']
    side = ['<a class="sitem" href="#overview" data-id="overview"><span class="sn">★</span>Tổng quan &amp; lộ trình</a>']
    for gi, (gkey, gname, gsub, ls) in enumerate(C["groups"]):
        color = GROUP_COLORS[gi % len(GROUP_COLORS)]
        side.append(f'<div class="sgroup" style="color:{color}">{escape(gname)}<small>{escape(gsub)}</small></div>')
        for L in ls:
            i = lessons_all.index(L) + 1
            k = order.index((L["id"], L["title"]))
            html_lessons.append(render_lesson(C, L, i, len(lessons_all), gkey, gname, color, order[k - 1],
                                              order[k + 1] if k + 1 < len(order) else None))
            side.append(f'<a class="sitem" href="#{L["id"]}" data-id="{L["id"]}"><span class="sn">{i}</span>{escape(L.get("short", L["title"]))}<span class="tick">✓</span></a>')

    tpl = open(os.path.join(HERE, "course_template.html"), encoding="utf-8").read()
    g = C["gradient"]
    rep = {
        "{{PAGE_TITLE}}": escape(C["title"]),
        "{{H_SUB}}": C["header_sub"],
        "{{GRAD}}": ",".join(g),
        "{{SIDEBAR}}": "\n".join(side),
        "{{LESSONS}}": "\n".join(html_lessons),
        "{{TOTAL}}": str(len(lessons_all)),
        "{{ORDER}}": json.dumps([o[0] for o in order]),
        "{{STORE}}": C["storage"],
        "{{SHORT}}": escape(C["short_title"]),
    }
    for k, v in rep.items():
        tpl = tpl.replace(k, v)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(tpl)
    print(f"Đã ghi {out_path} ({len(tpl) // 1024} KB, {len(lessons_all)} bài)")
