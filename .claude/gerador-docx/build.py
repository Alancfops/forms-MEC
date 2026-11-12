# -*- coding: utf-8 -*-
"""Gera o Documento de Requisitos do Projeto Fabiana substituindo o conteúdo
do modelo do TCC (mesmas seções, mesma formatação). Seções fora do escopo atual
(RNF, Segurança, Risco, Ponto de função) ficam só com títulos/tabelas vazias.

uso: python3 build.py <saida.docx> [pages.json]
"""
import sys, re, os, zipfile, json
from xml.sax.saxutils import escape as esc
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from split import split_body
import conteudo as C

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modelo-tcc.docx")
OUT = sys.argv[1]
PAGES = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else {}
NOME = C.SISTEMA

z = zipfile.ZipFile(SRC)
files = {n: z.read(n) for n in z.namelist()}
x = files['word/document.xml'].decode('utf-8')
pre, els, post = split_body(x)

FONT = '<w:rFonts w:ascii="Calibri" w:cs="Calibri" w:eastAsia="Calibri" w:hAnsi="Calibri"/>'
B = '<w:b w:val="1"/><w:bCs w:val="1"/>'
SUP = '<w:vertAlign w:val="superscript"/>'

def R(text, rpr=""):
    return f'<w:r><w:rPr>{FONT}{rpr}<w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r>'
def P(runs, ppr=""):
    return f'<w:p><w:pPr>{ppr}<w:rPr>{FONT}</w:rPr></w:pPr>{runs}</w:p>'
def empty():
    return f'<w:p><w:pPr><w:rPr>{FONT}</w:rPr></w:pPr></w:p>'
def texts(e):
    return ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', e))
def blank_texts(e):
    return re.sub(r'(<w:t(?: [^>]*)?>)[^<]*(</w:t>)', r'\1\2', e)
def nome_sistema(e):
    for old in ('SÊNIOR TESTE FUNCIONAL', 'Sênior teste funcional', 'Sênior Teste Funcional', 'Sênior Test Funcional'):
        e = e.replace(old, esc(NOME.upper() if old.isupper() else NOME))
    return e

out = list(els)

# ---- capa / introdução / ponto de função: só o nome do sistema
for k in (1, 8, 86, 93, 98):
    out[k] = nome_sistema(out[k])
out[2] = out[2].replace('ÉRIKA PRADO', esc(C.AUTOR))
# escopo da contagem de PF: o modelo dizia "sem integrações externas", o que não vale aqui
out[89] = nome_sistema(out[89]).replace(', vale salientar que o sistema está limitado aos módulos internos e não integrações com sistemas externos.', '.')

# ---- 2.1 Abrangência: substitui os 5 parágrafos
ppr31 = re.search(r'<w:pPr>.*?</w:pPr>', els[31], re.S).group(0)
for i, k in enumerate(range(31, 36)):
    out[k] = f'<w:p>{ppr31}{R(C.ABRANGENCIA[i])}</w:p>'

# ---- 3 Requisitos funcionais: mesma tabela, linhas novas
tbl = els[42]
tbl_head = tbl[:tbl.index('<w:tr>')]
header_row = re.findall(r'<w:tr>.*?</w:tr>', tbl, re.S)[0]
SP = '<w:spacing w:after="240" w:before="240" w:lineRule="auto"/>'
def rf_row(rf):
    cor = '<w:color w:val="000000"/>'
    idc = (f'<w:tc><w:tcPr/><w:p><w:pPr><w:jc w:val="center"/><w:rPr>{FONT}{B}{cor}</w:rPr></w:pPr>{R(rf["id"], B + cor)}</w:p></w:tc>')
    ps = [P(R(rf["titulo"], B)), empty(), P(R(rf["rot"], B))]
    for nome, q, sup, desc in rf["campos"]:
        runs = R(f"{nome} ({q})")
        if sup: runs += R(sup, SUP)
        runs += (f'<w:r><w:rPr>{FONT}<w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">:</w:t>'
                 f'<w:br w:type="textWrapping"/><w:t xml:space="preserve">{esc(desc)}</w:t></w:r>')
        ps.append(P(runs, SP))
    ps.append(P(R("Regras e observações dos campos:", B), SP))
    for i, rg in enumerate(rf["regras"], 1):
        ps.append(P(R(f"{i} ", SUP) + R(rg), SP))
    return f'<w:tr><w:trPr><w:cantSplit w:val="0"/><w:tblHeader w:val="0"/></w:trPr>{idc}<w:tc><w:tcPr/>{"".join(ps)}</w:tc></w:tr>'
out[42] = tbl_head + header_row + ''.join(rf_row(r) for r in C.RFS) + '</w:tbl>'

# ---- 4/5/6/8: só títulos -> tabelas mantidas com linhas vazias
def blank_rows(e, keep_header_rows=1, only_if=None):
    rows = re.findall(r'<w:tr\b.*?</w:tr>', e, re.S)
    for i, r in enumerate(rows):
        if i < keep_header_rows: continue
        if only_if and not re.search(only_if, texts(r)): continue
        e = e.replace(r, blank_texts(r), 1)
    return e
out[44] = blank_rows(els[44])                       # Requisito não funcional
out[47] = blank_rows(els[47])                       # Requisito de segurança
out[54] = re.sub(r'(<w:t(?: [^>]*)?>)[^<]*RS\d+[^<]*(</w:t>)', r'\1\2', els[54])  # Matriz de risco: tira os RS do TCC
out[100] = blank_rows(els[100], only_if=r'RF\d+')   # Ponto de função

# ---- 7 Matriz de rastreabilidade – RF
ids = [r["id"] for r in C.RFS]
W0 = 898; WC = (9180 - W0) // len(ids)
def mcell(text, shade=False):
    tcpr = '<w:tcPr><w:shd w:fill="bfbfbf" w:val="clear"/></w:tcPr>' if shade else '<w:tcPr/>'
    rpr = '<w:color w:val="000000"/><w:sz w:val="14"/><w:szCs w:val="14"/>'
    run = R(text, rpr) if text else ''
    return f'<w:tc>{tcpr}<w:p><w:pPr><w:jc w:val="center"/><w:rPr>{FONT}{rpr}</w:rPr></w:pPr>{run}</w:p></w:tc>'
mt_pr = re.search(r'<w:tblPr>.*?</w:tblPr>', els[58], re.S).group(0)
mt_pr = re.sub(r'<w:tblW [^>]*/>', f'<w:tblW w:w="{W0 + WC*len(ids)}" w:type="dxa"/>', mt_pr)
mt_pr = mt_pr.replace('<w:tblLook', '<w:tblCellMar><w:left w:w="40" w:type="dxa"/><w:right w:w="40" w:type="dxa"/></w:tblCellMar><w:tblLook')
grid = f'<w:gridCol w:w="{W0}"/>' + ''.join(f'<w:gridCol w:w="{WC}"/>' for _ in ids)
TR = '<w:tr><w:trPr><w:cantSplit w:val="0"/><w:tblHeader w:val="0"/></w:trPr>'
mt = f'<w:tbl>{mt_pr}<w:tblGrid>{grid}</w:tblGrid>'
mt += TR + mcell("ID de requisitos", True) + ''.join(mcell(i, True) for i in ids) + '</w:tr>'
for r in ids:
    mt += TR + mcell(r, True) + ''.join(mcell(C.MATRIZ.get(r, {}).get(c, "")) for c in ids) + '</w:tr>'
out[58] = mt + '</w:tbl>'

# ---- 9 Referências
ref_ppr = re.search(r'<w:pPr>.*?</w:pPr>', els[105], re.S).group(0)
out[105] = els[105] + ''.join(f'<w:p>{ref_ppr}{R(t)}</w:p>' for t in C.REFERENCIAS)  # mantém a referência do modelo

# ---- Sumário: mesmas entradas do modelo, só atualiza as páginas
headings = []
cnt = [0, 0, 0]
for e in els:
    m = re.search(r'<w:pStyle w:val="Heading(\d)"/>', e)
    a = re.search(r'w:name="(_[^"]+)"', e)
    if m and a:
        lv = int(m.group(1)); cnt[lv-1] += 1
        for i in range(lv, 3): cnt[i] = 0
        headings.append([lv, '.'.join(map(str, cnt[:lv])), texts(e).strip(), a.group(1)])
def upd_page(m):
    p = m.group(0)
    a = re.search(r'PAGEREF (\S+)', p)
    if a and a.group(1) in PAGES:
        p = re.sub(r'(<w:tab/><w:t xml:space="preserve">)\d*(</w:t>)', lambda mm: mm.group(1) + str(PAGES[a.group(1)]) + mm.group(2), p)
    return p
out[5] = re.sub(r'<w:p\b[^>]*>.*?</w:p>', upd_page, els[5], flags=re.S)

files['word/document.xml'] = (pre + ''.join(out) + post).encode('utf-8')
h = files['word/header1.xml'].decode('utf-8')
files['word/header1.xml'] = h.replace('SÊNIOR TESTE FUNCIONAL', esc(NOME.upper())).replace('ÉRIKA PRADO', esc(C.AUTOR)).encode('utf-8')
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zo:
    for n in z.namelist():
        zo.writestr(n, files[n])
json.dump(headings, open(os.path.join(HERE, 'headings.json'), 'w'), ensure_ascii=False)
print("ok", OUT, len(headings), "títulos")
