import re
def split_body(x):
    b0=x.index('<w:body>')+len('<w:body>'); b1=x.index('</w:body>')
    body=x[b0:b1]; els=[]; i=0
    while i<len(body):
        m=re.match(r'<w:(\w+)\b[^>]*?(/?)>',body[i:])
        tag=m.group(1)
        if m.group(2)=='/': els.append(body[i:i+m.end()]); i+=m.end(); continue
        depth=0; j=i
        pat=re.compile(r'<(/?)w:'+tag+r'\b[^>]*?(/?)>')
        for mm in pat.finditer(body,i):
            if mm.group(2)=='/': continue
            depth+= -1 if mm.group(1) else 1
            if depth==0: j=mm.end(); break
        els.append(body[i:j]); i=j
    return x[:b0],els,x[b1:]
