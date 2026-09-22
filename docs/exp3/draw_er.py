# -*- coding: utf-8 -*-
"""绘制广软广播站点歌与投稿系统 陈氏 E-R 图"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, FancyBboxPatch
from matplotlib.font_manager import FontProperties

FONT = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=11)
FONT_S = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=9)
FONT_E = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=12, weight="bold")
FONT_T = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=16, weight="bold")

C_ENT_FC, C_ENT_EC = "#DCE9F7", "#2E6DA4"
C_REL_FC, C_REL_EC = "#FDEFCB", "#D58E00"
C_ATT_FC, C_ATT_EC = "#EAF4E4", "#5B8C3E"

fig, ax = plt.subplots(figsize=(14.5, 9.2), dpi=150)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")


def entity(cx, cy, w, h, text):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.8",
                                fc=C_ENT_FC, ec=C_ENT_EC, lw=1.8, zorder=3))
    ax.text(cx, cy, text, ha="center", va="center", fontproperties=FONT_E, zorder=4)


def rel(cx, cy, w, h, text):
    pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
    ax.add_patch(Polygon(pts, closed=True, fc=C_REL_FC, ec=C_REL_EC, lw=1.6, zorder=3))
    ax.text(cx, cy, text, ha="center", va="center", fontproperties=FONT, zorder=4)


def attr(cx, cy, text, pk=False):
    disp = sum(2.0 if ord(c) > 0x2e80 else 1.0 for c in text)
    w = max(8.6, 1.6 + 0.72 * disp)
    ax.add_patch(Ellipse((cx, cy), width=w, height=5.2, fc=C_ATT_FC, ec=C_ATT_EC, lw=1.2, zorder=2))
    fp = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=9,
                        weight="bold" if pk else "normal")
    ax.text(cx, cy, text, ha="center", va="center", fontproperties=fp, zorder=3)
    if pk:
        ax.plot([cx - len(text) * 0.72, cx + len(text) * 0.72], [cy - 1.05, cy - 1.05],
                color="black", lw=0.9, zorder=3)


def line(p1, p2, z=1):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#444444", lw=1.3, zorder=z)


def card(x, y, text):
    ax.text(x, y, text, ha="center", va="center", fontproperties=FONT_S,
            bbox=dict(boxstyle="circle,pad=0.18", fc="white", ec="#B0B0B0", lw=0.8), zorder=5)


# ============ 实体位置 ============
USER = (50, 49)
SONG = (14, 80)
ART = (9, 31)
MSG = (37, 9)
AUD = (73, 9)
PGM = (84, 42)

# ============ 联系（菱形）位置 ============
R_SONG = (30, 66)
R_ART = (27, 40)
R_MSG = (43, 28)
R_AUD = (62, 28)
R_PGM = (70, 45)

# ============ 连线 ============
for u, r, e in [
    (USER, R_SONG, SONG),
    (USER, R_ART, ART),
    (USER, R_MSG, MSG),
    (USER, R_AUD, AUD),
    (USER, R_PGM, PGM),
]:
    line(u, r)
    line(r, e)

# 基数标签
card(40.5, 57.5, "1")
card(22.5, 73.5, "N")
card(37.5, 45.5, "1")
card(17.5, 35.5, "N")
card(46.5, 38.5, "1")
card(40.0, 18.5, "N")
card(55.5, 38.5, "1")
card(67.5, 18.5, "N")
card(60.0, 47.5, "1")
card(77.0, 43.7, "N")

# 角色注释（用户侧）
ax.text(43.2, 60.5, "学生", fontproperties=FONT_S, color="#8a5a00", ha="center")
ax.text(33.5, 47.8, "学生", fontproperties=FONT_S, color="#8a5a00", ha="center")
ax.text(49.0, 40.2, "用户", fontproperties=FONT_S, color="#8a5a00", ha="center")
ax.text(57.0, 40.6, "成员", fontproperties=FONT_S, color="#8a5a00", ha="center")
ax.text(62.5, 50.5, "成员", fontproperties=FONT_S, color="#8a5a00", ha="center")

# ============ 实体框 ============
entity(*USER, 12, 8, "用户 user")
entity(*SONG, 13, 8, "点歌单\nsong_request")
entity(*ART, 12, 8, "投稿文章\narticle")
entity(*MSG, 11, 8, "留言\nmessage")
entity(*AUD, 11, 8, "音频\naudio")
entity(*PGM, 13, 8, "节目单\nprogram_schedule")

# ============ 联系菱形 ============
rel(*R_SONG, 9, 7, "提交")
rel(*R_ART, 9, 7, "撰写")
rel(*R_MSG, 9, 7, "发表")
rel(*R_AUD, 9, 7, "上传")
rel(*R_PGM, 9, 7, "编排")

# ============ 属性（主键加下划线） ============
# 用户属性
for p, t, pk in [((45, 66), "id", True), ((54, 69), "username", False),
                 ((63, 65), "role", False), ((50, 74), "real_name", False)]:
    line(USER, p, z=0)
    attr(*p, t, pk)
# 点歌单属性
for p, t, pk in [((5, 90), "id", True), ((15, 93.5), "song_name", False),
                 ((25, 90), "singer", False), ((28, 80), "status", False)]:
    line(SONG, p, z=0)
    attr(*p, t, pk)
# 投稿文章属性
for p, t, pk in [((4.5, 23.5), "id", True), ((12.5, 18), "title", False),
                 ((20.5, 22), "type", False), ((22, 32), "status", False)]:
    line(ART, p, z=0)
    attr(*p, t, pk)
# 留言属性
for p, t, pk in [((27, 4.5), "id", True), ((37, 2.8), "content", False),
                 ((48, 4.5), "reply", False), ((50, 13.5), "status", False)]:
    line(MSG, p, z=0)
    attr(*p, t, pk)
# 音频属性
for p, t, pk in [((62, 4.5), "id", True), ((72, 2.8), "title", False),
                 ((83, 4.5), "file_path", False), ((85, 14), "play_count", False)]:
    line(AUD, p, z=0)
    attr(*p, t, pk)
# 节目单属性
for p, t, pk in [((94, 53), "id", True), ((94.6, 46), "program_name", False),
                 ((95, 38), "date", False), ((83, 57), "time_slot", False)]:
    line(PGM, p, z=0)
    attr(*p, t, pk)

# ============ 标题 ============
ax.text(50, 98, "图1  广软广播站点歌与投稿系统 E-R 图（陈氏表示法）",
        ha="center", va="center", fontproperties=FONT_T)

# ============ 图例（右上） ============
ax.add_patch(FancyBboxPatch((68.5, 90.6), 5.5, 3.6, boxstyle="round,pad=0.02,rounding_size=0.5",
                            fc=C_ENT_FC, ec=C_ENT_EC, lw=1.4))
ax.text(71.25, 92.4, "实体", ha="center", va="center", fontproperties=FONT_S)
ax.add_patch(Polygon([(79.5, 93.9), (82, 92.4), (79.5, 90.9), (77, 92.4)],
                     closed=True, fc=C_REL_FC, ec=C_REL_EC, lw=1.2))
ax.text(79.5, 89.3, "联系", ha="center", va="center", fontproperties=FONT_S)
ax.add_patch(Ellipse((88, 92.4), 5.2, 3.2, fc=C_ATT_FC, ec=C_ATT_EC, lw=1.2))
ax.text(88, 89.3, "属性", ha="center", va="center", fontproperties=FONT_S)

# 说明文字（上方中部空白带）
ax.text(52, 86.2, "说明：带下划线的属性为主键；五个联系基数均为 1:N，不存在 M:N 联系，故无需拆分中间表；\n各实体完整属性见“逻辑结构设计”关系模式表。",
        ha="center", va="center", fontproperties=FONT_S)

plt.tight_layout()
out = r"C:\Users\yyxyz\IdeaProjects\broadcast-system\docs\exp3\er_chen.png"
plt.savefig(out, bbox_inches="tight", facecolor="white")
print("saved", out)
