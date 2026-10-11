import ast,sys,os
root=sys.argv[1]; seeds=sys.argv[2:]
mods={}
for d,_,fs in os.walk(root):
    for f in fs:
        if f.endswith('.py'):
            p=os.path.relpath(os.path.join(d,f),root); m=p[:-3].replace('/','.')
            mods[m]=p
def imports(p,pkg):
    t=ast.parse(open(os.path.join(root,p),encoding='utf-8').read())
    out=set()
    for n in ast.walk(t):
        if isinstance(n,ast.Import):
            for a in n.names: out.add(a.name)
        elif isinstance(n,ast.ImportFrom):
            base=n.module or ''
            if n.level:
                parts=pkg.split('.')[:len(pkg.split('.'))-n.level+1]
                base='.'.join([x for x in parts if x]+([base] if base else []))
            out.add(base)
            for a in n.names: out.add(base+'.'+a.name if base else a.name)
    return {m for m in out if m in mods}
seen=set(); todo=[s[:-3].replace('/','.') for s in seeds]
while todo:
    m=todo.pop()
    if m in seen: continue
    seen.add(m); pkg='.'.join(m.split('.')[:-1])
    for x in imports(mods[m],pkg): todo.append(x)
for m in sorted(seen-{s[:-3].replace('/','.') for s in seeds}): print(mods[m])
