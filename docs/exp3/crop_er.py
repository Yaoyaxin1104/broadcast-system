# -*- coding: utf-8 -*-
from PIL import Image
src = r"C:\Users\yyxyz\IdeaProjects\broadcast-system\docs\exp3\er_chen.png"
im = Image.open(src)
w, h = im.size
# 裁掉顶部标题行（约前 68 像素），保留右上角图例
crop = im.crop((0, 68, w, h))
out = r"C:\Users\yyxyz\IdeaProjects\broadcast-system\docs\exp3\er_chen_hw1.png"
crop.save(out)
print(out, crop.size)
