# -*- coding: utf-8 -*-
import zipfile, os
src = r"F:\学号-姓名-作业1-Web应用项目需求分析与系统设计报告.docx"
out = r"C:\Users\yyxyz\IdeaProjects\broadcast-system\docs\exp3\placeholders"
os.makedirs(out, exist_ok=True)
z = zipfile.ZipFile(src)
for n in z.namelist():
    if n.startswith("word/media/") and not n.endswith("/"):
        data = z.read(n)
        open(os.path.join(out, os.path.basename(n)), "wb").write(data)
        print(os.path.basename(n), len(data))
