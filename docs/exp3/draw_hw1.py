# -*- coding: utf-8 -*-
"""作业1 图表绘制：登录时序图、功能模块图、用例图"""
import os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Ellipse, FancyArrowPatch, Polygon
from matplotlib.lines import Line2D

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = r"C:\Users\yyxyz\IdeaProjects\broadcast-system\docs\exp3"

BLUE_D = "#1F4E79"
BLUE_M = "#2E75B6"
BLUE_L = "#DEEAF6"
BLUE_LL = "#EAF2FB"
GRAY = "#595959"
ARROW = "#333333"

def rbox(ax, x, y, w, h, fc, ec, lw=1.2, rounded=0.35, z=2, text=None, fs=11, tc="black", bold=False, r=0.18):
    box = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                         boxstyle="round,pad=0,rounding_size=%s" % r,
                         fc=fc, ec=ec, lw=lw, zorder=z)
    ax.add_patch(box)
    if text is not None:
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc,
                zorder=z + 1, fontweight="bold" if bold else "normal")
    return box

def arrow(ax, x1, y1, x2, y2, dashed=False, lw=1.3, color=ARROW, fs=9.5, text=None,
          text_dy=1.4, z=3, head=7):
    ls = (0, (5, 3)) if dashed else "-"
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=head,
                        lw=lw, color=color, linestyle=ls, zorder=z, shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + text_dy, text, ha="center", va="bottom",
                fontsize=fs, color="#222", zorder=z + 1,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))

# ============================================================
# 1. 登录时序图
# ============================================================
def draw_sequence():
    fig, ax = plt.subplots(figsize=(13.6, 9.6), dpi=200)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    xs = [7, 23, 40, 57, 74, 91]
    names = ["用户", "前端页面", "UserController", "UserServiceImpl", "UserMapper", "MySQL"]

    # actor stick & db cylinder, others boxes
    def stick(ax, x, y):
        ax.add_line(Line2D([x, x], [y - 1.2, y - 4.2], color=ARROW, lw=1.3, zorder=4))
        ax.add_line(Line2D([x - 1.6, x + 1.6], [y - 2.4, y - 2.4], color=ARROW, lw=1.3, zorder=4))
        ax.add_line(Line2D([x, x - 1.6], [y - 4.2, y - 6.6], color=ARROW, lw=1.3, zorder=4))
        ax.add_line(Line2D([x, x + 1.6], [y - 4.2, y - 6.6], color=ARROW, lw=1.3, zorder=4))
        ax.add_patch(plt.Circle((x, y), 1.1, fc="white", ec=ARROW, lw=1.3, zorder=4))

    def cylinder(ax, x, y, w=7.5, h=5.2):
        ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=BLUE_LL, ec=BLUE_D, lw=1.2, zorder=3))
        ax.add_patch(plt.Circle((x, y + h / 2), w / 2, fc=BLUE_LL, ec=BLUE_D, lw=1.2, zorder=3))
        ax.add_patch(plt.Circle((x, y - h / 2), w / 2, fc="white", ec=BLUE_D, lw=1.2, zorder=3))

    stick(ax, xs[0], 95.2)
    ax.text(xs[0], 86.5, "用户", ha="center", fontsize=11, fontweight="bold")
    for i in range(1, 5):
        rbox(ax, xs[i], 92, 13.5, 5.2, BLUE_L, BLUE_D, fs=10.5, text=names[i], bold=True)
    cylinder(ax, xs[5], 92, w=6.8, h=4.6)
    ax.text(xs[5], 84.0, "MySQL", ha="center", fontsize=11, fontweight="bold")

    top, bottom = 88.5, 7
    for x in xs:
        ax.add_line(Line2D([x, x], [top, bottom], color=GRAY, lw=1.0, ls=(0, (4, 3)), zorder=1))

    def actbar(x, y1, y2, w=1.5):
        ax.add_patch(Rectangle((x - w / 2, y2), w, y1 - y2, fc=BLUE_L, ec=BLUE_M, lw=0.8, zorder=2))

    actbar(xs[2], 77, 14)
    actbar(xs[3], 72, 38)
    actbar(xs[4], 67, 52)
    actbar(xs[5], 62, 57)

    arrow(ax, xs[0], 82, xs[1], 82, text="输入用户名与密码")
    arrow(ax, xs[1], 77, xs[2], 77, text="POST /api/user/login")
    arrow(ax, xs[2], 72, xs[3], 72, text="login(username, password)")
    arrow(ax, xs[3], 67, xs[4], 67, text="findByUsername(username)")
    arrow(ax, xs[4], 62, xs[5], 62, text="SELECT * FROM user WHERE username = ?", fs=9)
    arrow(ax, xs[5], 57, xs[4], 57, dashed=True, text="用户记录（含 MD5 密文）")
    arrow(ax, xs[4], 52, xs[3], 52, dashed=True, text="User 对象")
    # self message at service
    arrow(ax, xs[3], 48, xs[3] + 6.5, 48, fs=9, text="MD5(输入密码) 与库中密文比对")
    ax.add_line(Line2D([xs[3] + 6.5, xs[3] + 6.5], [48, 45.2], color=ARROW, lw=1.2, zorder=3))
    a = FancyArrowPatch((xs[3] + 6.5, 45.2), (xs[3] + 0.2, 45.2), arrowstyle="-|>",
                        mutation_scale=7, lw=1.2, color=ARROW, zorder=3)
    ax.add_patch(a)

    # alt frame
    ax.add_patch(Rectangle((3, 8), 94, 36, fc="none", ec=GRAY, lw=1.2, zorder=1.5))
    ax.add_patch(Rectangle((3, 41.2), 8.5, 2.8, fc="#F2F2F2", ec=GRAY, lw=1.0, zorder=1.6))
    ax.text(7.2, 42.6, "alt", ha="center", va="center", fontsize=10, fontweight="bold", zorder=2)
    ax.text(13, 42.6, "[ 校验通过 ]", ha="left", va="center", fontsize=9.5, zorder=2)
    ax.add_line(Line2D([3, 97], [20.5, 20.5], color=GRAY, lw=1.0, zorder=1.5))
    ax.text(13, 21.6, "[ 校验失败 ]", ha="left", va="center", fontsize=9.5, zorder=2)

    arrow(ax, xs[3], 38, xs[2], 38, dashed=True, text="User 对象")
    arrow(ax, xs[2], 33, xs[2] + 6.5, 33, fs=9, text="session 写入 user")
    ax.add_line(Line2D([xs[2] + 6.5, xs[2] + 6.5], [33, 30.2], color=ARROW, lw=1.2, zorder=3))
    ax.add_patch(FancyArrowPatch((xs[2] + 6.5, 30.2), (xs[2] + 0.2, 30.2),
                                 arrowstyle="-|>", mutation_scale=7, lw=1.2, color=ARROW, zorder=3))
    arrow(ax, xs[2], 27, xs[1], 27, dashed=True, text="Result.success(user)")
    arrow(ax, xs[1], 23, xs[0], 23, dashed=True, text="跳转首页")
    arrow(ax, xs[2], 16, xs[1], 16, dashed=True, text='Result.error("用户名或密码错误")', fs=9)
    arrow(ax, xs[1], 11, xs[0], 11, dashed=True, text="显示错误提示")

    fig.tight_layout()
    p = os.path.join(OUT, "hw1_seq_login.png")
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", p)

# ============================================================
# 2. 功能模块图
# ============================================================
def draw_modules():
    fig, ax = plt.subplots(figsize=(13.8, 9.4), dpi=200)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

    rbox(ax, 50, 95, 34, 6.2, BLUE_D, BLUE_D, fs=13, text="广软广播站点歌与投稿系统", tc="white", bold=True, r=0.6)

    cards = [
        ("用户管理", ["用户注册", "用户登录", "查看 / 修改个人信息", "退出登录"]),
        ("点歌管理", ["提交点歌申请", "查看我的点歌", "点歌审核", "点歌搜索 / 安排播放"]),
        ("投稿管理", ["文章投稿", "我的投稿", "稿件审核", "稿件搜索"]),
        ("音频管理", ["音频上传", "音频列表试听", "音频下载", "音频删除"]),
        ("留言管理", ["发表留言", "留言列表", "留言回复", "留言搜索"]),
        ("节目单管理", ["节目编排", "节目发布", "节目查询", "节目搜索"]),
    ]
    cxs = [17.5, 50, 82.5]
    W, H = 29, 31
    tops = [82, 40]

    # connectors (behind cards)
    ax.add_line(Line2D([50, 50], [91.9, 8], color=BLUE_M, lw=1.4, zorder=1))
    bus_ys = [88, 46]
    card_top_ys = [tops[0], tops[1]]
    for yb, ct in zip(bus_ys, card_top_ys):
        ax.add_line(Line2D([cxs[0], cxs[2]], [yb, yb], color=BLUE_M, lw=1.4, zorder=1))
        for x in cxs:
            ax.add_line(Line2D([x, x], [yb, ct], color=BLUE_M, lw=1.4, zorder=1))

    for idx, (title, items) in enumerate(cards):
        row, col = divmod(idx, 3)
        x, ytop = cxs[col], tops[row]
        cy = ytop - H / 2
        ax.add_patch(FancyBboxPatch((x - W / 2, cy - H / 2), W, H,
                                    boxstyle="round,pad=0,rounding_size=0.5",
                                    fc="white", ec=BLUE_D, lw=1.3, zorder=2))
        ax.add_patch(FancyBboxPatch((x - W / 2, ytop - 5), W, 5,
                                    boxstyle="round,pad=0,rounding_size=0.5",
                                    fc=BLUE_M, ec=BLUE_M, lw=1.0, zorder=3))
        ax.add_patch(Rectangle((x - W / 2, ytop - 5), W, 2.2, fc=BLUE_M, ec="none", zorder=3))
        ax.text(x, ytop - 2.5, title, ha="center", va="center", fontsize=12.5,
                color="white", fontweight="bold", zorder=4)
        for j, it in enumerate(items):
            yy = ytop - 9.5 - j * 5.2
            ax.add_patch(plt.Circle((x - W / 2 + 3.2, yy), 0.45, fc=BLUE_M, ec="none", zorder=3))
            ax.text(x - W / 2 + 5.2, yy, it, ha="left", va="center", fontsize=11, zorder=3)

    fig.tight_layout()
    p = os.path.join(OUT, "hw1_modules.png")
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", p)

# ============================================================
# 3. 用例图
# ============================================================
def draw_usecase():
    fig, ax = plt.subplots(figsize=(13.8, 9.6), dpi=200)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

    # boundary
    ax.add_patch(Rectangle((21, 6), 60, 88, fc="white", ec=BLUE_D, lw=1.6, zorder=1))
    ax.text(51, 91.5, "广软广播站点歌与投稿系统", ha="center", va="center",
            fontsize=12.5, fontweight="bold", color=BLUE_D)

    def actor(x, y, name):
        ax.add_patch(plt.Circle((x, y + 4.4), 1.5, fc="white", ec=ARROW, lw=1.3, zorder=4))
        ax.add_line(Line2D([x, x], [y + 2.9, y - 1.5], color=ARROW, lw=1.3, zorder=4))
        ax.add_line(Line2D([x - 2.3, x + 2.3], [y + 1.0, y + 1.0], color=ARROW, lw=1.3, zorder=4))
        ax.add_line(Line2D([x, x - 2.1], [y - 1.5, y - 5], color=ARROW, lw=1.3, zorder=4))
        ax.add_line(Line2D([x, x + 2.1], [y - 1.5, y - 5], color=ARROW, lw=1.3, zorder=4))
        ax.text(x, y - 7.2, name, ha="center", fontsize=11.5, fontweight="bold")

    actor(9, 66, "学生")
    actor(9, 28, "教师")
    actor(91, 52, "广播站成员")

    EW, EH = 16.5, 6.6
    ell = {}
    def uc(key, x, y, label, fc=BLUE_LL):
        e = Ellipse((x, y), EW, EH, fc=fc, ec=BLUE_D, lw=1.2, zorder=3)
        ax.add_patch(e)
        ax.text(x, y, label, ha="center", va="center", fontsize=9.8, zorder=4)
        ell[key] = (x, y)

    # left column
    uc("reg", 32, 85, "注册账号")
    uc("song", 32, 75, "提交点歌")
    uc("art", 32, 65, "投稿文章")
    uc("msg", 32, 55, "发表留言")
    uc("mine", 32, 45, "查看我的点歌/投稿")
    # center shared
    uc("bprog", 51, 82, "浏览节目单")
    uc("baudio", 51, 72, "在线试听音频")
    uc("bart", 51, 62, "浏览投稿文章")
    uc("bmsg", 51, 52, "查看留言与回复")
    # right staff
    uc("asong", 70, 84, "审核点歌")
    uc("aart", 70, 74, "审核投稿")
    uc("uaudio", 70, 64, "上传音频")
    uc("prog", 70, 54, "编排发布节目单")
    uc("rmsg", 70, 44, "回复留言")
    uc("del", 70, 34, "内容删除管理")
    # login bottom center
    uc("login", 51, 20, "登录", fc="#FCE4D6")

    def edge(x, y, ux, uy):
        dx, dy = ux - x, uy - y
        a, b = EW / 2, EH / 2
        t = 1 / math.sqrt((dx / a) ** 2 + (dy / b) ** 2)
        return ux - dx * t, uy - dy * t

    def assoc(ax_pt, key, dashed=False):
        x, y = ax_pt
        ux, uy = ell[key]
        ex, ey = edge(x, y, ux, uy)
        ls = (0, (4, 3)) if dashed else "-"
        ax.add_line(Line2D([x, ex], [y, ey], color=ARROW, lw=1.0, ls=ls, zorder=2))

    stu = (9, 66)
    for k in ["reg", "song", "art", "msg", "mine", "bprog", "baudio", "bart", "bmsg"]:
        assoc(stu, k)
    tea = (9, 28)
    for k in ["bprog", "baudio", "bart", "bmsg"]:
        assoc(tea, k)
    staff = (91, 52)
    for k in ["asong", "aart", "uaudio", "prog", "rmsg", "del", "bprog", "baudio"]:
        assoc(staff, k)

    # include -> login (dashed)
    for k in ["song", "art", "msg", "asong", "aart", "uaudio", "prog", "rmsg", "del"]:
        assoc((ell[k][0] + 1, ell[k][1] - EH / 2 + 0.5), "login", dashed=True)
    ax.text(51, 12.2, "«include»", ha="center", fontsize=9, color=GRAY, style="italic")

    fig.tight_layout()
    p = os.path.join(OUT, "hw1_usecase.png")
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", p)

draw_sequence()
draw_modules()
draw_usecase()
print("ALL DONE")
