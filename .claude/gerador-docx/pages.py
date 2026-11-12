import subprocess,json,sys
pdf=sys.argv[1]
n=int([l for l in subprocess.run(['pdfinfo',pdf],capture_output=True,text=True).stdout.splitlines() if l.startswith('Pages')][0].split()[-1])
txt=[subprocess.run(['pdftotext','-f',str(i),'-l',str(i),'-layout',pdf,'-'],capture_output=True,text=True).stdout for i in range(1,n+1)]
toc_page=next(i for i,t in enumerate(txt) if 'Sumário' in t)
H=json.load(open('headings.json')); out={}
for l,num,t,a in H:
    for i in range(toc_page+1,n):
        if any(line.strip().endswith(t) and num in line for line in txt[i].splitlines()):
            out[a]=i+1; break
    else: out[a]='?'
print(n,out); json.dump(out,open('pages.json','w'))
