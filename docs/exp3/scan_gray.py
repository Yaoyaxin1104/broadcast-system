# -*- coding: utf-8 -*-
from docx import Document
from docx.oxml.ns import qn
doc = Document(r"C:\Users\yyxyz\IdeaProjects\broadcast-system\作业1-Web应用项目需求分析与系统设计报告（已完成）.docx")
for i, p in enumerate(doc.paragraphs):
    colors = set()
    for r in p.runs:
        rPr = r._element.find(qn("w:rPr"))
        if rPr is not None:
            c = rPr.find(qn("w:color"))
            if c is not None:
                colors.add(c.get(qn("w:val")))
    t = p.text.strip()
    if t and (t.startswith(("【", "写作说明")) or colors):
        print(i, colors, repr(t[:70]))
