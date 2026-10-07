# -*- coding: utf-8 -*-
"""生成接口文档单文件 HTML：广软广播站点歌与投稿系统"""
import html as H

OUT = r"C:\Users\yyxyz\IdeaProjects\broadcast-system\接口文档-广软广播站点歌与投稿系统.html"

# endpoint: (method, url, auth, desc, params[(loc,name,type,req,desc)], req_example, resp_example)
def E(m, u, auth, desc, params=None, req=None, resp=None):
    return dict(m=m, u=u, auth=auth, desc=desc, params=params or [], req=req, resp=resp)

modules = [
 ("user", "用户模块", [
  E("POST","/user/register","否","用户注册，密码经 MD5 加密后存储",
    [("body","username","String","是","登录账号，唯一"),
     ("body","password","String","是","登录密码"),
     ("body","role","String","是","角色：student/staff/teacher"),
     ("body","realName","String","否","真实姓名"),
     ("body","studentId","String","否","学号"),
     ("body","phone","String","否","联系电话"),
     ("body","email","String","否","邮箱")],
    '{\n  "username": "student1",\n  "password": "123456",\n  "realName": "张一",\n  "studentId": "2024001",\n  "role": "student",\n  "phone": "13800000001",\n  "email": "student1@example.com"\n}',
    '{\n  "code": 200,\n  "msg": "注册成功",\n  "data": null\n}'),
  E("POST","/user/login","否","用户登录，校验通过后用户信息写入 HttpSession，响应头返回 JSESSIONID Cookie",
    [("body","username","String","是","登录账号"),
     ("body","password","String","是","登录密码")],
    '{\n  "username": "student1",\n  "password": "123456"\n}',
    '{\n  "code": 200,\n  "msg": "success",\n  "data": {\n    "id": 1,\n    "username": "student1",\n    "realName": "张一",\n    "role": "student",\n    "status": 1\n  }\n}'),
  E("GET","/user/info","是","获取当前登录用户信息，从 Session 读取",
    [], None,
    '{\n  "code": 200,\n  "msg": "success",\n  "data": { "id": 1, "username": "student1", "role": "student" }\n}'),
  E("POST","/user/logout","是","退出登录，清除 Session 中的用户信息",
    [], None,
    '{\n  "code": 200,\n  "msg": "退出成功",\n  "data": null\n}'),
 ]),

 ("song", "点歌模块", [
  E("POST","/song/add?userId={userId}","学生","学生提交点歌申请，初始状态为 pending",
    [("query","userId","Long","是","学生用户ID"),
     ("body","songName","String","是","歌曲名称"),
     ("body","singer","String","是","歌手"),
     ("body","message","String","否","点歌留言")],
    '?userId=1\n{\n  "songName": "晴天",\n  "singer": "周杰伦",\n  "message": "午间时段播放，谢谢广播站！"\n}',
    '{\n  "code": 200,\n  "msg": "提交成功",\n  "data": null\n}'),
  E("GET","/song/my?userId={userId}","是","查询本人的点歌记录",
    [("query","userId","Long","是","学生用户ID")], None,
    '{\n  "code": 200,\n  "msg": "success",\n  "data": [ { "id": 1, "songName": "晴天", "status": "approved" } ]\n}'),
  E("GET","/song/list","是","查询全部点歌（LEFT JOIN user 返回学生信息）",
    [], None,
    '{\n  "code": 200,\n  "msg": "success",\n  "data": [ { "id": 1, "songName": "晴天", "singer": "周杰伦", "username": "student1", "status": "approved" } ]\n}'),
  E("GET","/song/detail/{id}","是","按ID查询点歌详情",
    [("path","id","Long","是","点歌单ID")]),
  E("GET","/song/pending","广播站成员","查询待审核点歌，从 Session 校验 staff 角色",
    [], None,
    '{\n  "code": 200,\n  "msg": "success",\n  "data": [ { "id": 2, "songName": "稻香", "status": "pending" } ]\n}'),
  E("PUT","/song/audit/{id}?status={status}&userId={userId}","广播站成员","审核点歌，记录审核结果与审核时间",
    [("path","id","Long","是","点歌单ID"),
     ("query","status","String","是","审核结果：approved/rejected"),
     ("query","userId","Long","是","操作成员ID")],
    'PUT /song/audit/2?status=approved&userId=3',
    '{\n  "code": 200,\n  "msg": "审核完成",\n  "data": null\n}'),
  E("DELETE","/song/delete/{id}","是","按ID删除点歌",
    [("path","id","Long","是","点歌单ID")], None,
    '{\n  "code": 200,\n  "msg": "删除成功",\n  "data": null\n}'),
  E("PUT","/song/update","是","修改点歌信息",
    [("body","SongRequest","Object","是","点歌单完整对象（须含 id）")],
    '{\n  "id": 2,\n  "songName": "稻香",\n  "singer": "周杰伦",\n  "status": "pending"\n}'),
  E("GET","/song/search?keyword={keyword}&status={status}","否","按歌曲名/歌手关键字与状态组合搜索，按申请时间倒序",
    [("query","keyword","String","否","歌曲名或歌手关键字"),
     ("query","status","String","否","审核状态")]),
 ]),

 ("article", "投稿模块", [
  E("POST","/article/add?userId={userId}","学生","提交投稿文章",
    [("query","userId","Long","是","学生用户ID"),
     ("body","title","String","是","标题"),
     ("body","content","String","是","正文内容"),
     ("body","type","String","是","类型：news/story/poem")],
    '?userId=1\n{\n  "title": "青春飞扬，梦想起航",\n  "content": "九月，我们怀揣梦想走进广软校园……",\n  "type": "poem"\n}',
    '{\n  "code": 200,\n  "msg": "投稿成功",\n  "data": null\n}'),
  E("GET","/article/search?title={title}&status={status}","否","按标题与状态搜索稿件",
    [("query","title","String","否","标题关键字"),
     ("query","status","String","否","审核状态")]),
  E("PUT","/article/update","是","修改稿件",
    [("body","Article","Object","是","稿件完整对象（须含 id）")]),
  E("GET","/article/detail/{id}","否","按ID查询稿件详情",
    [("path","id","Long","是","稿件ID")]),
  E("DELETE","/article/delete/{id}","是","按ID删除稿件",
    [("path","id","Long","是","稿件ID")]),
  E("PUT","/article/audit/{id}?status={status}&userId={userId}","广播站成员","审核稿件，记录审核结果与时间",
    [("path","id","Long","是","稿件ID"),
     ("query","status","String","是","approved/rejected"),
     ("query","userId","Long","是","操作成员ID")],
    'PUT /article/audit/2?status=approved&userId=3',
    '{\n  "code": 200,\n  "msg": "审核完成",\n  "data": null\n}'),
  E("GET","/article/list","否","查询全部稿件", []),
  E("GET","/article/pending","广播站成员","查询待审核稿件", []),
 ]),

 ("audio", "音频模块", [
  E("POST","/audio/upload","广播站成员","上传节目音频（multipart/form-data），文件以 UUID 重命名存储，数据库保存元数据",
    [("form","file","File","是","音频文件，大小不超过 50MB"),
     ("form","title","String","是","音频标题"),
     ("form","userId","Long","是","操作成员ID")],
    'Content-Type: multipart/form-data\nfile: <音频文件>\ntitle: 晴天\nuserId: 3',
    '{\n  "code": 200,\n  "msg": "上传成功",\n  "data": null\n}'),
  E("GET","/audio/download/{id}","否","按ID下载音频文件（二进制流）",
    [("path","id","Long","是","音频ID")], None,
    '响应为 application/octet_stream 二进制文件流'),
  E("GET","/audio/list","否","查询在线音频（status=1，按上传时间倒序）",
    [], None,
    '{\n  "code": 200,\n  "msg": "success",\n  "data": [ { "id": 1, "title": "晴天", "playCount": 35, "duration": 269 } ]\n}'),
  E("DELETE","/audio/delete/{id}","广播站成员","按ID删除音频",
    [("path","id","Long","是","音频ID")]),
 ]),

 ("message", "留言模块", [
  E("POST","/message/add?userId={userId}","是","发表留言",
    [("query","userId","Long","是","留言用户ID"),
     ("body","content","String","是","留言内容")],
    '?userId=1\n{\n  "content": "广播站的节目越来越精彩了！希望多放一些流行歌曲。"\n}',
    '{\n  "code": 200,\n  "msg": "留言成功",\n  "data": null\n}'),
  E("DELETE","/message/delete/{id}","广播站成员","按ID删除留言",
    [("path","id","Long","是","留言ID")]),
  E("PUT","/message/reply/{id}?reply={reply}&userId={userId}","广播站成员","回复留言",
    [("path","id","Long","是","留言ID"),
     ("query","reply","String","是","回复内容"),
     ("query","userId","Long","是","操作成员ID")],
    'PUT /message/reply/1?reply=感谢支持，本周午间已安排流行专场&userId=3',
    '{\n  "code": 200,\n  "msg": "回复成功",\n  "data": null\n}'),
  E("GET","/message/search?content={content}","否","按内容关键字搜索留言",
    [("query","content","String","是","关键字")]),
  E("GET","/message/list","否","查询留言列表（含回复，按时间倒序）",
    [], None,
    '{\n  "code": 200,\n  "msg": "success",\n  "data": [ { "id": 1, "content": "节目越来越精彩了！", "reply": "感谢支持" } ]\n}'),
 ]),

 ("program", "节目单模块", [
  E("POST","/program/publish?userId={userId}","广播站成员","发布节目单，状态置为 published 并记录发布时间",
    [("query","userId","Long","是","操作成员ID"),
     ("body","date","Date","是","节目日期，如 2026-09-21"),
     ("body","timeSlot","String","是","时间段，如 12:00-12:30"),
     ("body","programName","String","是","节目名称"),
     ("body","content","String","否","节目内容"),
     ("body","songs","String","否","播放歌单快照")],
    '?userId=3\n{\n  "date": "2026-09-21",\n  "timeSlot": "12:00-12:30",\n  "programName": "音乐午高峰",\n  "content": "流行音乐点播与祝福放送。",\n  "songs": "晴天；夜曲；兰亭序"\n}',
    '{\n  "code": 200,\n  "msg": "发布成功",\n  "data": null\n}'),
  E("DELETE","/program/delete/{id}","广播站成员","按ID删除节目单",
    [("path","id","Long","是","节目单ID")]),
  E("GET","/program/list","否","查询全部节目单", []),
  E("PUT","/program/update","广播站成员","修改节目单",
    [("body","ProgramSchedule","Object","是","节目单完整对象（须含 id）")]),
  E("GET","/program/detail/{id}","否","按ID查询节目单详情",
    [("path","id","Long","是","节目单ID")]),
  E("GET","/program/search?programName={programName}&date={date}","否","按节目名称与日期搜索节目单",
    [("query","programName","String","否","节目名称关键字"),
     ("query","date","Date","否","节目日期")]),
 ]),
]

errors = [
 ("200","操作成功","请求正常处理完成"),
 ("400","请求参数有误","缺少必填参数或参数格式不合法"),
 ("401","未登录或登录已过期","Session 中无登录信息或登录状态失效"),
 ("403","没有操作权限","角色不符，或调用了非本角色可用的接口"),
 ("404","请求的资源不存在","访问了不存在的资源 ID 或文件"),
 ("409","数据冲突","用户名已存在等重复数据场景"),
 ("500","系统内部错误","服务端未预期的异常"),
 ("1001","业务处理失败","业务流程未满足预期，如审核状态不合法"),
]

def esc(s):
    return H.escape(str(s))

nav = "".join('<a href="#sec-%s">%s</a>' % (k, t) for k, t, _ in modules)

sec_html = []
idx = 0
for k, t, eps in modules:
    cards = []
    for e in eps:
        idx += 1
        badge = '<span class="badge m-%s">%s</span>' % (e["m"], e["m"])
        auth = '<span class="auth">鉴权：%s</span>' % esc(e["auth"])
        params = ""
        if e["params"]:
            rows = "".join(
                "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                % (esc(loc), esc(n), esc(ty), esc(rq), esc(d))
                for loc, n, ty, rq, d in e["params"])
            params = ('<div class="sub">请求参数</div><table class="pt">'
                      '<tr><th>位置</th><th>参数</th><th>类型</th><th>必填</th><th>说明</th></tr>'
                      '%s</table>') % rows
        ex = ""
        if e["req"]:
            ex += '<div class="sub">请求示例</div><pre>%s</pre>' % esc(e["req"])
        if e["resp"]:
            ex += '<div class="sub">响应示例</div><pre>%s</pre>' % esc(e["resp"])
        cards.append(
            '<div class="card" id="ep-%d"><div class="chead">%s<span class="url">%s</span>%s</div>'
            '<div class="cdesc">%s</div>%s%s</div>'
            % (idx, badge, esc(e["u"]), auth, esc(e["desc"]), params, ex))
    sec_html.append('<section id="sec-%s"><h2>%s</h2>%s</section>' % (k, esc(t), "".join(cards)))

err_rows = "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>"
                   % (c, m, d) for c, m, d in errors)

page = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>接口文档 - 广软广播站点歌与投稿系统</title>
<style>
:root{--d:#1F4E79;--m:#2E75B6;--l:#DEEAF6;--bg:#f4f7fb;}
*{box-sizing:border-box;}
body{margin:0;font-family:"Microsoft YaHei","Segoe UI",Arial,sans-serif;color:#222;background:var(--bg);line-height:1.6;}
header{background:linear-gradient(120deg,#1F4E79,#2E75B6);color:#fff;padding:34px 40px;}
header h1{margin:0 0 8px;font-size:26px;}
header .meta{font-size:14px;opacity:.92;}
header code{background:rgba(255,255,255,.18);padding:2px 8px;border-radius:4px;font-size:13px;}
.layout{display:flex;max-width:1280px;margin:0 auto;}
nav{width:210px;flex:none;padding:24px 14px;position:sticky;top:0;align-self:flex-start;}
nav a{display:block;padding:8px 12px;color:#1F4E79;text-decoration:none;border-radius:6px;font-size:14px;}
nav a:hover{background:var(--l);}
main{flex:1;padding:24px 30px 60px;min-width:0;}
.gen{background:#fff;border:1px solid #d8e2ee;border-radius:10px;padding:18px 22px;margin-bottom:26px;}
.gen h3{margin:14px 0 8px;color:var(--d);font-size:15px;}
.gen h3:first-child{margin-top:0;}
.gen ul{margin:6px 0;padding-left:22px;font-size:13.5px;}
pre{background:#1e2b38;color:#e6edf5;padding:12px 14px;border-radius:8px;font-family:Consolas,"Courier New",monospace;
 font-size:12.5px;overflow-x:auto;margin:6px 0 4px;line-height:1.5;white-space:pre-wrap;word-break:break-word;}
h2{color:var(--d);border-left:5px solid var(--m);padding-left:10px;font-size:19px;margin:34px 0 14px;}
.card{background:#fff;border:1px solid #d8e2ee;border-radius:10px;margin:14px 0;overflow:hidden;}
.chead{padding:11px 16px;background:#f0f5fb;display:flex;align-items:center;gap:10px;flex-wrap:wrap;}
.url{font-family:Consolas,monospace;font-size:13px;font-weight:bold;color:#16375a;word-break:break-all;}
.auth{margin-left:auto;font-size:12px;color:#666;}
.badge{font-family:Consolas,monospace;font-size:11.5px;font-weight:bold;color:#fff;padding:2px 9px;border-radius:5px;min-width:62px;text-align:center;display:inline-block;}
.m-GET{background:#2e9e5b;}.m-POST{background:#2E75B6;}.m-PUT{background:#d39222;}.m-DELETE{background:#c0453d;}
.cdesc{padding:10px 16px 2px;font-size:13.5px;color:#444;}
.sub{padding:10px 16px 0;font-size:12.5px;font-weight:bold;color:var(--d);}
table{width:100%;border-collapse:collapse;font-size:12.5px;margin:6px 16px 8px;width:calc(100% - 32px);}
.pt{display:table;}
th,td{border:1px solid #d3ddea;padding:6px 9px;text-align:left;vertical-align:top;}
th{background:var(--l);color:#16375a;}
main pre{margin:6px 16px 10px;}
footer{text-align:center;color:#888;font-size:12.5px;padding:26px;}
@media(max-width:860px){nav{display:none;}main{padding:16px;}}
</style></head><body>
<header>
 <h1>广软广播站点歌与投稿系统 · 接口文档</h1>
 <div class="meta">技术栈：Spring Boot 2.7 + MyBatis-Plus + MySQL 8.0 &nbsp;|&nbsp; 版本：v1.0</div>
 <div class="meta">Base URL：<code>http://localhost:8089/api</code></div>
</header>
<div class="layout">
 <nav>__NAV__</nav>
 <main>
  <div class="gen">
   <h3>一、通用约定</h3>
   <ul>
    <li>接口 URL 采用“/api/模块/动作”约定，/api 为应用上下文路径；以 HTTP 方法区分操作：POST 新增/登录、GET 查询、PUT 修改/审核、DELETE 删除。</li>
    <li>除文件上传外，请求体与响应体均为 application/json；文件上传使用 multipart/form-data。</li>
    <li>所有接口统一返回 Result 结构：<code>{ "code": 状态码, "msg": 提示信息, "data": 业务数据 }</code>。</li>
   </ul>
   <h3>二、鉴权说明</h3>
   <ul>
    <li>系统基于 <b>HttpSession</b> 维护登录状态：登录成功后用户对象写入 Session，浏览器通过 JSESSIONID Cookie 保持会话。</li>
    <li>需要身份的接口从 Session 读取用户（部分接口通过 userId 参数结合角色校验）；未登录返回“未登录”，角色不符返回“无权限”。</li>
    <li>用户密码经 <b>MD5</b> 摘要后存储，数据库中不保存明文密码。</li>
   </ul>
   <h3>三、统一错误码</h3>
   <table style="width:100%;margin:6px 0">
    <tr><th>错误码</th><th>含义</th><th>触发场景</th></tr>__ERR__
   </table>
  </div>
  __SEC__
 </main>
</div>
<footer>广软广播站点歌与投稿系统 接口文档 · 共 __N__ 个接口</footer>
</body></html>"""

page = page.replace("__NAV__", nav).replace("__ERR__", err_rows)
page = page.replace("__SEC__", "".join(sec_html)).replace("__N__", str(idx))
open(OUT, "w", encoding="utf-8").write(page)
print("SAVED:", OUT, "endpoints:", idx)
