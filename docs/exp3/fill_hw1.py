# -*- coding: utf-8 -*-
"""填充作业1：Web应用项目需求分析与系统设计报告（广软广播站点歌与投稿系统）"""
import os, copy, shutil
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph
from PIL import Image

SRC = r"F:\学号-姓名-作业1-Web应用项目需求分析与系统设计报告.docx"
TGT = r"C:\Users\yyxyz\IdeaProjects\broadcast-system\作业1-Web应用项目需求分析与系统设计报告（已完成）.docx"
ROOT = r"C:\Users\yyxyz\IdeaProjects\broadcast-system"
IMGD = os.path.join(ROOT, "docs", "exp3")

shutil.copyfile(SRC, TGT)
doc = Document(TGT)
sec = doc.sections[0]
AVAIL_CM = (sec.page_width - sec.left_margin - sec.right_margin) / 360000
print("avail cm:", AVAIL_CM)

# ---------------- helpers ----------------
def style_run(r, size=12, bold=False, code=False, ea="宋体"):
    r.bold = bold
    r.font.size = Pt(size)
    name = "Courier New" if code else "Times New Roman"
    r.font.name = name
    rPr = r._element.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rPr.insert(0, rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs"):
        rf.set(qn(a), name)
    rf.set(qn("w:eastAsia"), ea)

def clear_runs(p):
    for r in list(p.runs):
        r._element.getparent().remove(r._element)

def body_fmt(p, indent_chars=200, line=360, center=False):
    pPr = p._p.get_or_add_pPr()
    ind = pPr.find(qn("w:ind"))
    if ind is None:
        ind = OxmlElement("w:ind"); pPr.append(ind)
    if center:
        ind.set(qn("w:firstLine"), "0"); ind.set(qn("w:firstLineChars"), "0")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        ind.set(qn("w:firstLineChars"), str(indent_chars))
        ind.set(qn("w:firstLine"), str(int(240 * indent_chars / 100)))
    sp = pPr.find(qn("w:spacing"))
    if sp is None:
        sp = OxmlElement("w:spacing"); pPr.append(sp)
    sp.set(qn("w:before"), "0"); sp.set(qn("w:after"), "0")
    sp.set(qn("w:line"), str(line)); sp.set(qn("w:lineRule"), "auto")

def write_body(p, text, size=12, center=False, bold=False):
    clear_runs(p)
    body_fmt(p, center=center)
    r = p.add_run(text)
    style_run(r, size=size, bold=bold)

def new_p_after(cursor_p):
    np = OxmlElement("w:p")
    cursor_p._p.addnext(np)
    return Paragraph(np, cursor_p._parent)

def replace_with(p, texts, size=12):
    write_body(p, texts[0], size=size)
    cur = p
    for t in texts[1:]:
        np = new_p_after(cur)
        write_body(np, t, size=size)
        cur = np

def delete_p(p):
    p._p.getparent().remove(p._p)

def overwrite_keepfmt(p, new):
    runs = p.runs
    if not runs:
        p.add_run(new); return
    runs[0].text = new
    for r in runs[1:]:
        r._element.getparent().remove(r._element)

def cell_set(cell, text, size=9.5, bold=False, center=False):
    p = cell.paragraphs[0]
    clear_runs(p)
    pPr = p._p.get_or_add_pPr()
    ind = pPr.find(qn("w:ind"))
    if ind is None:
        ind = OxmlElement("w:ind"); pPr.append(ind)
    ind.set(qn("w:firstLine"), "0"); ind.set(qn("w:firstLineChars"), "0")
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    style_run(r, size=size, bold=bold)

def rebuild_table(tbl, data, size=9.5, center_cols=()):
    tmpl = copy.deepcopy(tbl.rows[1]._tr)
    for r in tbl.rows[1:]:
        r._tr.getparent().remove(r._tr)
    for row in data:
        tbl._tbl.append(copy.deepcopy(tmpl))
    for ri, row in enumerate(tbl.rows[1:]):
        vals = data[ri]
        for ci, v in enumerate(vals):
            cell_set(row.cells[ci], v, size=size, center=(ci in center_cols))

# ---------------- 1. 替换图片 ----------------
img_map = {"rId8": "hw1_seq_login.png", "rId9": "hw1_modules.png",
           "rId10": "hw1_usecase.png", "rId11": "er_chen_hw1.png"}
for p in doc.paragraphs:
    blips = p._p.findall(".//" + qn("a:blip"))
    if not blips:
        continue
    rid = blips[0].get(qn("r:embed"))
    if rid not in img_map:
        continue
    path = os.path.join(IMGD, img_map[rid])
    iw, ih = Image.open(path).size
    w = AVAIL_CM
    h = w * ih / iw
    if h > 21:
        h = 21; w = h * iw / ih
    clear_runs(p)
    body_fmt(p, center=True)
    run = p.add_run()
    run.add_picture(path, width=Cm(w))
    print("image swapped:", rid, img_map[rid])

# ---------------- 2. 图题 ----------------
cap_map = {"图3-1用户登录流程时序图": "图3-1 用户登录流程时序图",
           "图3-2系统功能模块图": "图3-2 系统功能模块图",
           "图3-3系统用例图": "图3-3 系统用例图",
           "图4-1系统E-R图": "图4-1 系统 E-R 图"}
for p in doc.paragraphs:
    t = p.text.strip()
    if t in cap_map:
        clear_runs(p)
        body_fmt(p, center=True)
        r = p.add_run(cap_map[t])
        style_run(r, size=10.5, bold=True)

# ---------------- 3. 正文（前缀 → 段落列表；None 表示删除） ----------------
RULES = [
 ("写作说明：以下为正文结构示例", None),

 ("本节采用“现状→问题→契机”三段式写法", [
 "校园广播是高校校园文化建设的重要载体。广州软件学院广播站在午间、傍晚等固定时段面向全校师生播出音乐、新闻与互动节目，是传递校园资讯、服务师生生活的重要窗口。长期以来，广播站的点歌与投稿环节主要依靠纸质登记表、QQ群留言等方式完成，存在信息分散、审核过程缺少留痕、节目编排依赖人工核对、节目音频资料难以沉淀和检索等问题。",
 "随着学校办学规模不断扩大，全日制在校生已达一万余人，广播站每周收到的点歌申请与投稿数量持续增长，传统人工处理方式在开学、军训、毕业季等业务高峰期容易出现漏审、错播、回复不及时等情况，师生的参与体验和广播站的运转效率都受到影响。",
 "本系统旨在为校园广播业务搭建一个集点歌、投稿、音频管理、留言互动与节目单编排于一体的Web平台，实现申请在线提交、审核全程留痕、节目单统一发布、音频资料集中管理，从而减轻广播站成员的事务性工作量，提升师生参与度，丰富校园文化生活。"]),

 ("本节对2~3个同类系统进行简要分析", [
 "通过对同类系统与相关产品的调研，可以将现有方案分为以下三类。",
 "第一类是高校学生自研的校园广播点歌系统。这类系统多以点歌表单加后台审核为核心，支持按播出日期对点歌进行简单统计，在单一高校广播站有一定应用，但其功能普遍只覆盖点歌环节，不包含投稿、音频沉淀与节目单编排，模块较为单一，难以形成完整业务闭环。",
 "第二类是网络电台与商业音乐平台，如网易云音乐、喜马拉雅等。这类产品具备成熟的音频上传、播放计数与评论互动能力，用户体验好，但其面向公开互联网场景设计，账号体系与内容审核流程和校园广播的实名登记、定时段播出需求不匹配，也无法支撑按校园节目单对每日节目进行编排。",
 "第三类是部分高校建设的校园融媒体管理平台。这类平台统一汇聚校内多种媒体业务，功能全面，但体量庞大、建设与运维成本高，对于单一广播站的点歌、投稿业务而言过于厚重，难以快速落地。",
 "综合来看，现有方案中面向校园广播站、同时覆盖“点歌—投稿—审核—节目单—音频沉淀”完整闭环的轻量级系统较少，本系统正是针对这一空白进行设计与实现。"]),

 ("本节用3~4条概括本文完成的工作", [
 "本文围绕广软广播站点歌与投稿系统的设计与实现，主要完成以下工作。",
 "（1）调研校园广播站的实际业务流程，完成需求分析，明确学生、广播站成员、教师三类角色的功能边界，并使用用例图、功能模块图与时序图对系统进行建模；（2）完成系统总体架构、接口与数据库设计，采用Spring Boot、MyBatis-Plus与MySQL技术栈实现用户、点歌、投稿、音频、留言、节目单六大功能模块；（3）完成点歌审核、投稿审核、音频上传下载、节目单发布、留言回复等核心功能的开发，并对系统进行功能验证。"]),

 ("从技术栈成熟度、开发环境可获得性", [
 "系统后端采用Spring Boot 2.7、MyBatis-Plus 3.5与MySQL 8.0，均为成熟的开源技术，社区活跃、文档完善；开发使用IntelliJ IDEA、Maven与JDK 17，开发环境易于搭建。系统采用B/S架构，师生通过浏览器即可访问，无需安装专门的客户端，因此在技术上完全可行。"]),

 ("说明项目所需软件均为开源免费", [
 "系统所使用的Spring Boot、MyBatis-Plus、MySQL社区版等技术栈以及Git、Maven等工具均可免费获取，系统部署在校园内普通计算机或实验室服务器上即可运行，无需额外采购软硬件，建设与运行成本很低，经济上可行。"]),

 ("说明目标用户具备基本浏览器操作能力", [
 "系统的目标用户为在校师生与广播站成员，均具备基本的浏览器操作能力；系统以Web形式提供、无需安装客户端，界面按照实际业务流程设计，关键操作提供确认与错误提示，学习成本低，广播站成员经过简单说明即可完成审核、上传与编排工作，操作上可行。"]),

 ("本节梳理核心业务流程，说明每个角色的职责与操作路径", [
 "系统的核心业务流程如下：学生注册并登录后，可以在线提交点歌申请，填写歌曲名称、歌手与点歌留言，也可以提交新闻、故事、诗歌等类型的投稿文章；广播站成员登录后，对待审核的点歌与投稿进行审核，审核通过的点歌结合每日节目单安排播出，审核通过的投稿可在节目中朗读或在平台展示；成员还可以上传节目音频、编排并发布每日节目单。师生可以浏览节目单、在线试听音频、浏览投稿文章并发表留言，由广播站成员对留言进行回复。",
 "三类角色的业务定位各有侧重：学生主要进行点歌、投稿、留言以及查询本人的点歌与投稿记录；广播站成员负责内容审核、音频管理、节目单编排发布、留言回复与内容管理；教师主要浏览节目单、试听音频、浏览投稿并提出建议。用户登录这一核心流程的时序如图3-1所示。"]),

 ("至少绘制一个核心流程的时序图", None),

 ("本节按模块列出系统全部功能", [
 "按照MoSCoW方法对功能需求划分优先级，其中Must表示本期必须实现，Should表示应该实现，Could表示可以实现，Won't表示本期不会实现、列入后续规划。系统功能需求如表3-1所示，其中必须实现的功能约占全部功能的三分之二，保证核心业务闭环完整；系统功能模块如图3-2所示，系统用例如图3-3所示。"]),

 ("功能模块图用于呈现系统功能划分与层级关系", None),
 ("用例图用于表示参与者与系统功能之间的关系", None),

 ("非功能需求描述系统“做得怎么样”", [
 "除功能需求外，系统还应满足性能、安全、可用性、可维护性与可靠性等方面的非功能需求，各项指标须可量化、可验证，具体内容如表3-2所示。"]),

 ("说明系统采用分层架构，从请求入口到数据持久化", [
 "系统采用B/S架构与经典的分层结构进行设计。后端基于Spring Boot 2.7.14搭建，持久层使用MyBatis-Plus 3.5.3，数据库采用MySQL 8.0并通过Druid连接池管理连接；前端使用HTML、CSS与JavaScript编写页面，通过HTTP接口与后端交互，后端以统一的Result结构返回数据。系统各层次的职责与关键实现如表4-1所示。"]),
 ("分层设计的核心是职责分离", None),

 ("本节在3.3节功能需求的基础上", [
 "系统在功能需求的基础上按照高内聚、低耦合的原则划分为六个模块。用户模块以HttpSession为中心管理注册、登录与退出状态；点歌模块与投稿模块采用统一的“提交—待审核—审核”状态流转设计，以状态字段记录pending、approved、rejected，审核时同步写入审核时间；音频模块将音频文件以UUID重命名后存储到服务器磁盘，数据库仅保存标题、路径、大小等元数据；留言模块支持留言与成员回复；节目单模块按日期与时段编排节目，并维护草稿与已发布两种状态。各模块通过Service层对外提供业务能力，模块之间以用户标识进行逻辑关联、不直接耦合，便于独立开发与测试。"]),

 ("本节设计核心业务接口，须符合RESTful规范", [
 "系统按照业务划分为用户、点歌、投稿、音频、留言、节目单六个模块。接口URL采用“/api/模块/动作”的约定，其中/api为应用上下文路径，并以HTTP方法区分操作类型：POST表示注册、登录、提交等动作，GET表示查询，PUT表示修改与审核，DELETE表示删除。相较于严格的名词复数式REST风格，“模块加动作”的URL表意直接、与校园业务术语一致，便于课程项目的前后端协作与接口调试。",
 "系统的登录状态基于HttpSession维护：用户登录成功后，其用户对象写入服务器端Session；需要身份识别的接口从Session中读取登录用户，或结合用户参数校验角色，未登录或角色不符时返回相应的错误提示。系统核心接口清单如表4-1所示，接口错误码约定如下表所示。"]),

 ("本节基于需求分析识别实体、属性与关系", [
 "对系统业务数据进行抽象，得到用户、点歌单、投稿文章、音频、留言、节目单六个实体。其中，一个学生用户可以提交多条点歌单和多篇投稿文章，一个广播站成员可以上传多个音频、编排多个节目单、回复多条留言，一个用户可以发表多条留言，上述联系均为一对多联系。系统的E-R图如图4-1所示。"]),
 ("E-R图设计须遵守以下要求", None),

 ("在E-R模型基础上转换为关系模式", [
 "将概念模型转换为关系模型，并结合业务需要补充字段类型、约束与索引，得到系统的全部数据库表，各表字段设计如表4-2所示。"]),

 ("索引设计须基于实际查询场景", [
 "在物理结构设计上，表间关联采用“逻辑外键加普通索引”的方式：关联列建立普通索引，但不建立数据库级的外键约束，以降低批量导入与内容维护时表与表之间的耦合、提升操作灵活性，关联完整性由应用层校验保证；当业务需要数据库层强一致时，可执行建表脚本末尾以注释形式给出的物理外键语句。结合各类高频查询场景设计的索引如下表所示。"]),

 ("本表为作业必交附件，须如实填写", None),
]

for prefix, texts in RULES:
    hit = None
    for p in doc.paragraphs:
        if p.text.strip().startswith(prefix):
            hit = p; break
    if hit is None:
        print("NOT FOUND:", prefix)
        continue
    if texts is None:
        delete_p(hit)
    else:
        replace_with(hit, texts, size=12)

# ---------------- 4. 表格标题 ----------------
title_map = {
 "表3-1系统功能需求清单": "表3-1 系统功能需求清单",
 "表3-2系统非功能需求表": "表3-2 系统非功能需求表",
 "表4-1核心接口清单": "表4-1 核心接口清单",
 "表4-2数据库表设计（数据库user表）": "表4-2 数据库表设计",
}
for p in doc.paragraphs:
    t = p.text.strip()
    if t in title_map:
        overwrite_keepfmt(p, title_map[t])

# 检查清单中与本设计不符的条目改写
for p in doc.paragraphs:
    if p.text.strip().startswith("□接口URL均为名词复数"):
        overwrite_keepfmt(p, "□接口URL约定统一、表意清晰，接口文档要素齐全；")

# ---------------- 5. 表格内容 ----------------
tables = doc.tables

func_rows = [
 ["F-01","用户管理","用户注册","学生提交用户名、密码、真实姓名、学号等完成注册，密码经MD5加密后存储","M"],
 ["F-02","用户管理","用户登录","校验用户名与密码，成功后将用户信息写入HttpSession","M"],
 ["F-03","用户管理","查看个人信息","登录用户查看本人资料，需登录","M"],
 ["F-04","用户管理","退出登录","清除Session中的登录状态","M"],
 ["F-05","点歌管理","提交点歌","学生填写歌曲名、歌手、点歌留言后提交，初始状态为待审核","M"],
 ["F-06","点歌管理","我的点歌","学生查看本人点歌记录及审核状态","M"],
 ["F-07","点歌管理","点歌审核","广播站成员审核点歌，填写通过或驳回结果并记录审核时间","M"],
 ["F-08","点歌管理","点歌搜索","按歌曲名、歌手关键字与状态组合搜索点歌","S"],
 ["F-09","点歌管理","安排播放","记录审核通过点歌的实际播放时间","S"],
 ["F-10","投稿管理","文章投稿","学生提交新闻、故事、诗歌类型的稿件","M"],
 ["F-11","投稿管理","我的投稿","学生查看本人投稿记录及审核状态","M"],
 ["F-12","投稿管理","稿件审核","成员审核稿件，记录审核结果与审核时间","M"],
 ["F-13","投稿管理","稿件搜索","按标题关键字与状态搜索稿件","S"],
 ["F-14","音频管理","音频上传","成员上传节目音频，记录标题、文件大小等信息","M"],
 ["F-15","音频管理","音频列表","展示在线音频，按上传时间倒序浏览","M"],
 ["F-16","音频管理","音频下载试听","提供音频文件下载与在线播放","M"],
 ["F-17","音频管理","音频删除","成员删除失效音频","S"],
 ["F-18","留言管理","发表留言","登录用户发表留言","M"],
 ["F-19","留言管理","留言回复","广播站成员回复师生留言","S"],
 ["F-20","留言管理","留言搜索","按内容关键字搜索留言","S"],
 ["F-21","节目单管理","编排节目单","成员编排每日节目单，填写日期、时段、节目名称、内容与歌单","M"],
 ["F-22","节目单管理","发布节目单","发布节目单并记录发布时间","M"],
 ["F-23","节目单管理","节目单搜索","按节目名称与日期搜索节目单","M"],
 ["F-24","系统支撑","定时任务","定时统计音频播放量等运行数据","C"],
 ["F-25","——","在线直播","本期不实现音频实时直播，列入后续版本规划","W"],
 ["F-26","——","移动App与支付打赏","本期不开发移动客户端，不提供在线支付与打赏功能","W"],
]
rebuild_table(tables[2], func_rows, size=9, center_cols=(0,4))

nfr_rows = [
 ["性能","页面与接口响应速度","常规页面打开不超过2秒；核心查询接口在校园网环境下响应不超过1秒","浏览器开发者工具与接口工具多次测量取均值"],
 ["性能","并发承载能力","满足广播站日常业务量，支持约100名用户同时在线操作","使用JMeter进行并发测试"],
 ["安全","密码存储","密码经MD5摘要后存储，数据库中不出现明文密码","检查数据库password字段内容"],
 ["安全","访问控制","管理类接口仅广播站成员可调用，未登录或角色不符时返回错误提示","以不同角色账号交叉调用接口验证"],
 ["安全","文件上传安全","音频上传限定文件格式，大小不超过50MB，文件以UUID重命名","构造非法格式与超大文件验证"],
 ["可用性","浏览器兼容","支持Chrome、Edge主流浏览器最新两个大版本","在主流浏览器中逐项实测"],
 ["可用性","操作易用性","点歌、投稿等核心操作3步以内完成，页面提示信息清晰","按照业务流程走查"],
 ["可维护性","代码规范","采用分层架构，包结构清晰，关键逻辑配有注释","代码评审与走查"],
 ["可靠性","数据可靠性","审核、发布等关键操作结果即时持久化，服务重启后数据不丢失","重启服务后核对业务数据"],
]
rebuild_table(tables[3], nfr_rows, size=9)

layer_rows = [
 ["Controller层","接收请求、接收与校验参数、调用Service、以统一Result结构返回","@RestController、@RequestMapping、Result"],
 ["Service层","处理业务逻辑、控制事务","@Service、@Transactional"],
 ["Mapper层","数据访问，提供基础CRUD与自定义查询能力","MyBatis-Plus BaseMapper、Mapper XML"],
 ["公共模块","统一返回结构、错误码枚举、业务异常与全局异常处理","Result、ErrorCode、BizException、GlobalExceptionHandler"],
]
for ri, vals in enumerate(layer_rows):
    for ci, v in enumerate(vals):
        cell_set(tables[4].rows[ri + 1].cells[ci], v, size=10)

api_rows = [
 ["API-01","POST","/api/user/register","用户注册","否"],
 ["API-02","POST","/api/user/login","用户登录，登录信息写入Session","否"],
 ["API-03","GET","/api/user/info","获取当前登录用户信息","是"],
 ["API-04","POST","/api/user/logout","退出登录","是"],
 ["API-05","POST","/api/song/add?userId=","学生提交点歌申请","是"],
 ["API-06","GET","/api/song/my?userId=","查询本人的点歌记录","是"],
 ["API-07","GET","/api/song/list","查询全部点歌（含学生信息）","是"],
 ["API-08","GET","/api/song/pending","查询待审核点歌","是（成员）"],
 ["API-09","PUT","/api/song/audit/{id}?status=&userId=","审核点歌","是（成员）"],
 ["API-10","GET","/api/song/search?keyword=&status=","按关键字与状态搜索点歌","否"],
 ["API-11","POST","/api/article/add?userId=","提交投稿文章","是"],
 ["API-12","PUT","/api/article/audit/{id}?status=&userId=","审核投稿稿件","是（成员）"],
 ["API-13","GET","/api/article/list","查询全部稿件","否"],
 ["API-14","GET","/api/article/search?title=&status=","按标题与状态搜索稿件","否"],
 ["API-15","POST","/api/audio/upload","上传音频（multipart表单）","是（成员）"],
 ["API-16","GET","/api/audio/list","查询在线音频列表","否"],
 ["API-17","GET","/api/audio/download/{id}","下载音频文件","否"],
 ["API-18","POST","/api/message/add?userId=","发表留言","是"],
 ["API-19","PUT","/api/message/reply/{id}?reply=&userId=","回复留言","是（成员）"],
 ["API-20","GET","/api/message/list","查询留言列表","否"],
 ["API-21","POST","/api/program/publish?userId=","发布节目单","是（成员）"],
 ["API-22","GET","/api/program/list","查询节目单列表","否"],
 ["API-23","GET","/api/program/search?programName=&date=","按名称与日期搜索节目单","否"],
]
rebuild_table(tables[5], api_rows, size=8.8, center_cols=(0,1,4))

err_rows = [
 ["200","操作成功","请求正常处理完成"],
 ["400","请求参数有误","缺少必填参数或参数格式不合法"],
 ["401","未登录或登录已过期","Session中无登录信息或登录状态已失效"],
 ["403","没有操作权限","角色不符，或调用了非本角色可用的接口"],
 ["404","请求的资源不存在","访问了不存在的资源ID或文件"],
 ["409","数据冲突","用户名已存在等重复数据场景"],
 ["500","系统内部错误","服务端未预期的异常"],
 ["1001","业务处理失败","业务流程未满足预期，如审核状态不合法"],
]
rebuild_table(tables[6], err_rows, size=9.2, center_cols=(0,))

def rows_for(table, fields):
    return [[table] + list(f) for f in fields]
db_rows = []
db_rows += rows_for("user", [
 ("id","BIGINT","PK, AUTO_INCREMENT","用户主键"),
 ("username","VARCHAR(50)","NOT NULL, UNIQUE","登录账号，唯一"),
 ("password","VARCHAR(255)","NOT NULL","密码MD5密文（32位）"),
 ("real_name","VARCHAR(50)","NULL","真实姓名"),
 ("student_id","VARCHAR(20)","NULL","学号"),
 ("role","VARCHAR(20)","NOT NULL","角色：student/staff/teacher"),
 ("phone","VARCHAR(20)","NULL","联系电话"),
 ("email","VARCHAR(100)","NULL","邮箱"),
 ("status","INT","NOT NULL, DEFAULT 1","状态：0禁用 1启用"),
 ("create_time","DATETIME","NOT NULL, DEFAULT CURRENT_TIMESTAMP","注册时间"),
])
db_rows += rows_for("song_request", [
 ("id","BIGINT","PK, AUTO_INCREMENT","点歌单主键"),
 ("student_id","BIGINT","NOT NULL, INDEX","点歌学生，逻辑外键→user.id"),
 ("song_name","VARCHAR(100)","NOT NULL","歌曲名称"),
 ("singer","VARCHAR(50)","NOT NULL","歌手"),
 ("message","VARCHAR(500)","NULL","点歌留言"),
 ("status","VARCHAR(20)","NOT NULL, DEFAULT 'pending'","pending/approved/rejected"),
 ("audit_time","DATETIME","NULL","审核时间"),
 ("play_time","DATETIME","NULL","播放时间"),
 ("create_time","DATETIME","NOT NULL, DEFAULT CURRENT_TIMESTAMP","申请时间"),
])
db_rows += rows_for("article", [
 ("id","BIGINT","PK, AUTO_INCREMENT","稿件主键"),
 ("student_id","BIGINT","NOT NULL, INDEX","投稿学生，逻辑外键→user.id"),
 ("title","VARCHAR(200)","NOT NULL","标题"),
 ("content","TEXT","NOT NULL","正文内容"),
 ("type","VARCHAR(20)","NOT NULL","类型：news/story/poem"),
 ("status","VARCHAR(20)","NOT NULL, DEFAULT 'pending'","pending/approved/rejected"),
 ("audit_time","DATETIME","NULL","审核时间"),
 ("create_time","DATETIME","NOT NULL, DEFAULT CURRENT_TIMESTAMP","投稿时间"),
])
db_rows += rows_for("audio", [
 ("id","BIGINT","PK, AUTO_INCREMENT","音频主键"),
 ("staff_id","BIGINT","NOT NULL, INDEX","上传成员，逻辑外键→user.id"),
 ("title","VARCHAR(100)","NOT NULL","音频标题"),
 ("file_path","VARCHAR(255)","NOT NULL","文件存储路径"),
 ("file_size","BIGINT","NULL","文件大小（字节）"),
 ("duration","INT","NULL","时长（秒）"),
 ("play_count","INT","NOT NULL, DEFAULT 0","播放次数"),
 ("status","INT","NOT NULL, DEFAULT 1","状态：0下线 1上线"),
 ("create_time","DATETIME","NOT NULL, DEFAULT CURRENT_TIMESTAMP","上传时间"),
])
db_rows += rows_for("message", [
 ("id","BIGINT","PK, AUTO_INCREMENT","留言主键"),
 ("user_id","BIGINT","NOT NULL, INDEX","留言用户，逻辑外键→user.id"),
 ("content","VARCHAR(500)","NOT NULL","留言内容"),
 ("reply","VARCHAR(500)","NULL","回复内容"),
 ("status","INT","NOT NULL, DEFAULT 1","状态：0隐藏 1显示"),
 ("create_time","DATETIME","NOT NULL, DEFAULT CURRENT_TIMESTAMP","留言时间"),
])
db_rows += rows_for("program_schedule", [
 ("id","BIGINT","PK, AUTO_INCREMENT","节目单主键"),
 ("staff_id","BIGINT","NOT NULL, INDEX","编排成员，逻辑外键→user.id"),
 ("date","DATE","NOT NULL","节目日期"),
 ("time_slot","VARCHAR(20)","NOT NULL","时间段，如12:00-12:30"),
 ("program_name","VARCHAR(100)","NOT NULL","节目名称"),
 ("content","TEXT","NULL","节目内容"),
 ("songs","TEXT","NULL","播放歌单快照文本"),
 ("status","VARCHAR(20)","NOT NULL, DEFAULT 'draft'","draft/published"),
 ("publish_time","DATETIME","NULL","发布时间"),
 ("create_time","DATETIME","NOT NULL, DEFAULT CURRENT_TIMESTAMP","创建时间"),
])
rebuild_table(tables[7], db_rows, size=8.6)

idx_rows = [
 ["登录时按用户名精确查询用户","uk_username(username)，UNIQUE","唯一约束同时满足等值查询需求"],
 ["按角色筛选用户","idx_role(role)","支撑按学生、成员角色的查询"],
 ["学生查询本人点歌","idx_student_id(student_id)","加速“我的点歌”关联过滤"],
 ["成员按状态审核点歌","idx_status(status)","快速筛选待审核点歌"],
 ["学生查询本人投稿","idx_student_id(student_id)","加速“我的投稿”关联过滤"],
 ["成员按状态审核稿件","idx_status(status)","快速筛选待审核稿件"],
 ["成员查询上传的音频","idx_staff_id(staff_id)","按上传成员过滤音频"],
 ["按日期查询节目单","idx_date(date)","支撑按日期检索节目单"],
 ["按用户查询留言","idx_user_id(user_id)","加速用户留言的关联查询"],
]
rebuild_table(tables[8], idx_rows, size=9.2)

ai_rows = [
 ["豆包","需求分析与文档撰写","辅助梳理功能需求清单与章节文字；关键提示词：“根据点歌、投稿、审核的业务流程整理功能需求表，并按MoSCoW方法标注优先级”","逐条核对功能与实际代码是否一致，删除与项目不符的条目，重写项目背景等章节","约15%"],
 ["豆包","数据库设计","辅助检查建表SQL的字段类型与索引；关键提示词：“检查六张表的字段类型、逻辑外键与索引设计是否合理”","对照MySQL实际执行结果核对，保留原有命名与MD5口径","约10%"],
 ["豆包","接口文档","辅助生成接口文档初稿；关键提示词：“根据Controller源码整理接口的方法、URL、参数与响应示例”","逐个接口与源码比对修正，补充错误码与鉴权说明","约10%"],
]
rebuild_table(tables[9], ai_rows, size=8.8)

# ---------------- 6. 通用清理：残留灰字与示例 ----------------
to_del = []
for p in doc.paragraphs:
    t = p.text.strip()
    if t.startswith("【"):
        to_del.append(p); continue
    gray = False
    for r in p.runs:
        rPr = r._element.find(qn("w:rPr"))
        if rPr is not None:
            c = rPr.find(qn("w:color"))
            if c is not None and c.get(qn("w:val")) == "7F7F7F":
                gray = True; break
    if gray:
        to_del.append(p)
for p in to_del:
    delete_p(p)
print("cleanup deleted:", len(to_del))

doc.save(TGT)
print("SAVED:", TGT)
