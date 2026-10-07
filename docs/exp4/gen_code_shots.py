# -*- coding: utf-8 -*-
"""生成代码截图：HTML(自写 Java 高亮) -> headless Edge PNG"""
import os, re, html as htmlmod, subprocess, tempfile, shutil

ROOT = r'C:\Users\yyxyz\IdeaProjects\broadcast-system'
SRC = os.path.join(ROOT, 'src', 'main', 'java', 'com', 'grbroadcast')
OUT = os.path.join(ROOT, 'docs', 'exp4', 'shots')
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
os.makedirs(OUT, exist_ok=True)

KEYWORDS = set('''abstract assert boolean break byte case catch char class const continue
default do double else enum extends final finally float for goto if implements import
instanceof int interface long native new package private protected public return short
static strictfp super switch synchronized this throw throws transient try void volatile
while var record sealed permits yield'''.split())

TOKEN_RE = re.compile(
    r'(/\*[\s\S]*?\*/)'          # 1 block comment
    r'|(//[^\n]*)'               # 2 line comment
    r'|("(?:\\.|[^"\\])*")'      # 3 string
    r"|('(?:\\.|[^'\\])*')"      # 4 char
    r'|(@[A-Za-z_]\w*)'          # 5 annotation
    r'|(\b0x[\da-fA-F_]+\b|\b\d[\d_]*(?:\.\d+)?[fLdD]?\b)'  # 6 number
    r'|(\b[A-Z][A-Za-z0-9_]*\b)' # 7 type
    r'|(\b[a-z_]\w*(?=\s*\())'   # 8 method call
)

CSS = '''
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#212836;font-family:Consolas,"JetBrains Mono",monospace;}
.bar{height:42px;background:#181e2a;display:flex;align-items:center;padding:0 18px;}
.dot{width:12px;height:12px;border-radius:50%;margin-right:8px;display:inline-block;}
.fname{color:#9aa7bd;font-size:13px;margin-left:14px;}
.code{padding:14px 0 18px 0;font-size:14px;line-height:22px;color:#c8d3e0;
      white-space:pre;display:flex;}
.lnos{color:#4d5a70;text-align:right;padding:0 16px 0 22px;user-select:none;}
.lnos div,.lines div{height:22px;}
.lines{padding-right:26px;}
.block + .bar{border-top:6px solid #212836;}
.kw{color:#569cd6;}.str{color:#98c379;}.com{color:#6b7a90;font-style:italic;}
.ann{color:#dcdcaa;}.num{color:#d19a66;}.typ{color:#4ec9b0;}.mtd{color:#e5c07b;}
'''

def render_plain(seg):
    def plain_repl(mm):
        w = mm.group(0)
        if re.fullmatch(r'[A-Za-z_]\w*', w) and w in KEYWORDS:
            return f'<span class="kw">{w}</span>'
        return htmlmod.escape(w)
    return re.sub(r'[A-Za-z_]\w*|[^A-Za-z_]+', plain_repl, seg)

def highlight(code):
    out = []
    pos = 0
    for m in TOKEN_RE.finditer(code):
        if m.start() > pos:
            out.append(render_plain(code[pos:m.start()]))
        tok = m.group(0)
        esc = htmlmod.escape(tok)
        if m.group(1) is not None or m.group(2) is not None:
            out.append(f'<span class="com">{esc}</span>')
        elif m.group(3) is not None or m.group(4) is not None:
            out.append(f'<span class="str">{esc}</span>')
        elif m.group(5) is not None:
            out.append(f'<span class="ann">{esc}</span>')
        elif m.group(6) is not None:
            out.append(f'<span class="num">{esc}</span>')
        elif m.group(7) is not None:
            out.append(f'<span class="typ">{esc}</span>')
        elif m.group(8) is not None:
            out.append(f'<span class="mtd">{esc}</span>')
        pos = m.end()
    if pos < len(code):
        out.append(render_plain(code[pos:]))
    return ''.join(out)

def code_block(code, pre=False):
    lines = code.split('\n')
    n = len(lines)
    lnos = ''.join(f'<div>{i+1}</div>' for i in range(n))
    body = ''.join(f'<div>{(ln if pre else highlight(ln)) or " "}</div>' for ln in lines)
    return (f'<div class="code"><div class="lnos">{lnos}</div>'
            f'<div class="lines">{body}</div></div>')

def render(name, blocks):
    """blocks: list of (filename, code)"""
    html_parts = [f'<!doctype html><html><head><meta charset="utf-8">'
                  f'<style>{CSS}</style></head><body>']
    total_lines = 0
    for block in blocks:
        fname, code = block[0], block[1]
        pre = block[2] if len(block) > 2 else False
        html_parts.append(
            '<div class="bar">'
            '<span class="dot" style="background:#ff5f57"></span>'
            '<span class="dot" style="background:#febc2e"></span>'
            '<span class="dot" style="background:#28c840"></span>'
            f'<span class="fname">{fname}</span></div>'
            '<div class="block">')
        html_parts.append(code_block(code, pre))
        html_parts.append('</div>')
        total_lines += code.count('\n') + 1
    html_parts.append('</body></html>')
    h = 42 * len(blocks) + 22 * total_lines + 32
    w = 1280
    tmpdir = tempfile.mkdtemp(prefix='edgeshot_')
    hp = os.path.join(tmpdir, 'p.html')
    with open(hp, 'w', encoding='utf-8') as f:
        f.write(''.join(html_parts))
    png = os.path.join(OUT, name + '.png')
    cmd = [EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars',
           '--force-device-scale-factor=2', f'--user-data-dir={tmpdir}',
           f'--window-size={w},{h}', f'--screenshot={png}',
           'file:///' + hp.replace('\\', '/')]
    r = subprocess.run(cmd, capture_output=True, timeout=90)
    shutil.rmtree(tmpdir, ignore_errors=True)
    ok = os.path.exists(png)
    print(('OK ' if ok else 'FAIL ') + name)
    return ok

def read(rel):
    with open(os.path.join(SRC, rel.replace('/', os.sep)), encoding='utf-8') as f:
        return f.read()

def annotation_snippets(rel):
    lines = read(rel).split('\n')
    chunks, i = [], 0
    while i < len(lines):
        if '@PreAuthorize' in lines[i]:
            chunk = '\n'.join(lines[i:i + 3])
            chunks.append(chunk)
            i += 3
        else:
            i += 1
    return '\n\n'.join(chunks)

XML_RE = re.compile(
    r'(<!--[\s\S]*?-->)'
    r'|(</?[A-Za-z][\w\-.]*)'
    r'|([A-Za-z][\w:.-]*=)'
    r'|("(?:\\.|[^"\\])*")'
    r'|([<>/?])'
)
def hl_xml(code):
    out, pos = [], 0
    for m in XML_RE.finditer(code):
        if m.start() > pos:
            out.append(htmlmod.escape(code[pos:m.start()]))
        t, e = m.group(0), htmlmod.escape(m.group(0))
        if m.group(1): out.append(f'<span class="com">{e}</span>')
        elif m.group(2): out.append(f'<span class="kw">{e}</span>')
        elif m.group(3): out.append(f'<span class="ann">{e}</span>')
        elif m.group(4): out.append(f'<span class="str">{e}</span>')
        else: out.append(f'<span style="color:#8896ad">{e}</span>')
        pos = m.end()
    if pos < len(code): out.append(htmlmod.escape(code[pos:]))
    return ''.join(out)

def pom_snippet():
    with open(os.path.join(ROOT, 'pom.xml'), encoding='utf-8') as f:
        text = f.read()
    wanted = ('spring-boot-starter-security', 'spring-boot-starter-data-redis',
              'hutool-all', 'fastjson')
    blocks = re.findall(r'[ \t]*<dependency>.*?</dependency>\s*', text, re.S)
    picked = [b for b in blocks if any(w in b for w in wanted)]
    return hl_xml('<dependencies>\n' + ''.join(picked) + '</dependencies>')

JOBS = [
    ('code_pom', [('pom.xml（新增安全相关依赖）', pom_snippet(), True)]),
    ('code_redis', [('config/RedisConfig.java', read('config/RedisConfig.java'))]),
    ('code_jwt', [('utils/JwtUtil.java', read('utils/JwtUtil.java'))]),
    ('code_loginuser', [('security/LoginUser.java', read('security/LoginUser.java'))]),
    ('code_userdetails', [('security/UserDetailsServiceImpl.java',
                           read('security/UserDetailsServiceImpl.java'))]),
    ('code_filter', [('security/JwtAuthenticationTokenFilter.java',
                      read('security/JwtAuthenticationTokenFilter.java'))]),
    ('code_security', [('config/SecurityConfig.java',
                        read('config/SecurityConfig.java'))]),
    ('code_auth', [('controller/AuthController.java',
                    read('controller/AuthController.java'))]),
    ('code_handlers', [
        ('security/AuthenticationEntryPointImpl.java',
         read('security/AuthenticationEntryPointImpl.java')),
        ('security/AccessDeniedHandlerImpl.java',
         read('security/AccessDeniedHandlerImpl.java'))]),
    ('code_permservice', [('security/PermissionService.java',
                           read('security/PermissionService.java'))]),
    ('code_permmanager', [('security/PermissionManager.java',
                           read('security/PermissionManager.java'))]),
    ('code_menuservice', [('service/impl/MenuServiceImpl.java',
                           read('service/impl/MenuServiceImpl.java'))]),
    ('code_menucontroller', [('controller/MenuController.java',
                              read('controller/MenuController.java'))]),
    ('code_snip_song', [('controller/SongController.java（权限注解）',
                         annotation_snippets('controller/SongController.java'))]),
    ('code_snip_article', [('controller/ArticleController.java（权限注解）',
                            annotation_snippets('controller/ArticleController.java'))]),
    ('code_snip_audio', [('controller/AudioController.java（权限注解）',
                          annotation_snippets('controller/AudioController.java'))]),
    ('code_snip_message', [('controller/MessageController.java（权限注解）',
                            annotation_snippets('controller/MessageController.java'))]),
    ('code_snip_program', [('controller/ProgramController.java（权限注解）',
                            annotation_snippets('controller/ProgramController.java'))]),
]

if __name__ == '__main__':
    for name, blocks in JOBS:
        render(name, blocks)
