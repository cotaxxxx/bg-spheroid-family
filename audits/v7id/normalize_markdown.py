import sys,re
t=open(sys.argv[1],encoding='utf-8').read()
out=[]
for line in t.splitlines():
    s=line.strip()
    if re.fullmatch(r'[\-\|: ]*',s) : continue   # blank, ---, |---|---|
    s=re.sub(r'^#+\s*','',s)
    s=s.replace('**','').replace('`','')
    s=s.replace('|',' ').replace('\t',' ')
    s=re.sub(r'^[-*]\s+','- ',s)
    s=re.sub(r'\s+',' ',s).strip()
    if s: out.append(s)
print('\n'.join(out))
