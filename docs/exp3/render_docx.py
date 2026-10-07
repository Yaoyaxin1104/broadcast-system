# -*- coding: utf-8 -*-
"""docx -> 单文件 HTML（含图片），用于 headless 浏览器打印 PDF 目检"""
import os, sys
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

SRC = sys.argv[1]
OUTDIR = sys.argv[2]
os.makedirs(OUTDIR, exist_ok=True)
IMGDIR = os.path.join(OUTDIR, "img")
os.makedirs(IMGDIR, exist_ok=True)

doc = Document(SRC)

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def para_html(p):
    t = p.text
    style = p.style.name if p.style is not None else ""
    align = p.alignment
    # image?
    blips = p._p.findall(".//" + qn("a:blip"))
    imgs = []
    for b in blips:
        rid = b.get(qn("r:embed"))
        part = doc.part.related_parts.get(rid)
        if part is not None:
            ext = os.path.splitext(part.partname)[1] or ".png"
            fn = rid + ext
            open(os.path.join(IMGDIR, fn), "wb").write(part.blob)
            imgs.append("img/" + fn)
    inner = esc(t)
    for im in imgs:
        inner += '<br/><img src="%s"/>' % im
    cls = ""
    if style.startswith("Heading") or style.startswith("标题"):
        lvl = "".join(ch for ch in style if ch.isdigit()) or "1"
        tag = "h%s" % min(int(lvl), 4)
        return '<%s class="hd">%s</%s>' % (tag, inner, tag)
    if align is not None and str(align).endswith("CENTER (1)"):
        cls = ' class="ctr"'
    if t.strip().startswith(("图", "表")) and len(t.strip()) < 40:
        cls = ' class="ctr cap"'
    return "<p%s>%s</p>" % (cls, inner)

def table_html(tbl):
    s = ['<table border="1" cellspacing="0" cellpadding="4">']
    for ri, row in enumerate(tbl.rows):
        s.append("<tr>")
        for cell in row.cells:
            tag = "th" if ri == 0 else "td"
            ps = [para_html(p) for p in cell.paragraphs]
            s.append("<%s>%s</%s>" % (tag, "".join(ps), tag))
        s.append("</tr>")
    s.append("</table>")
    return "".join(s)

body = doc.element.body
parts = []
for child in body.iterchildren():
    if child.tag == qn("w:p"):
        parts.append(para_html(Paragraph(child, doc)))
    elif child.tag == qn("w:tbl"):
        parts.append(table_html(Table(child, doc)))

html = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@page { size: A4; margin: 2.5cm 2.6cm; }
body { font-family: "Times New Roman", SimSun, serif; font-size: 12pt; line-height: 1.5; color:#000; }
p { text-indent: 2em; margin: 0; }
p.ctr, p.cap { text-indent: 0; text-align: center; }
p.cap { font-size: 10.5pt; font-weight: bold; }
h1,h2,h3,h4 { font-family: "Times New Roman", SimHei, sans-serif; text-indent:0;
   page-break-after: avoid; margin: 10pt 0 6pt; }
h1 { font-size: 16pt; text-align:center; }
h2 { font-size: 14pt; }
h3 { font-size: 13pt; }
h4 { font-size: 12pt; }
table { border-collapse: collapse; width: 100%; margin: 6pt auto; font-size: 9pt; page-break-inside: avoid; }
th { background: #D9D9D9; font-weight: bold; text-align: center; }
td, th { vertical-align: top; }
td p, th p { text-indent: 0 !important; }
img { max-width: 100%; display:block; margin: 4pt auto; }
</style></head><body>
__BODY__
</body></html>"""
html = html.replace("__BODY__", "\n".join(parts))

out = os.path.join(OUTDIR, "render.html")
open(out, "w", encoding="utf-8").write(html)
print(out)
