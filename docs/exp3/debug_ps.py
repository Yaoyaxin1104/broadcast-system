# -*- coding: utf-8 -*-
from docx import Document
doc = Document(r"C:\Users\yyxyz\IdeaProjects\broadcast-system\作业1-Web应用项目需求分析与系统设计报告（已完成）.docx")
ps = doc.paragraphs
for i, p in enumerate(ps):
    t = p.text
    if t.strip():
        print(i, repr(t[:60]))
