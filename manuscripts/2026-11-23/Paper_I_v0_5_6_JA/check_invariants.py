"""Check that a Japanese translation of a LaTeX file keeps every formula, label, reference, citation, link and
path of the English file.  Display formulas are compared in order; inline formulas, refs and the rest as multisets
(Japanese word order may move them inside a sentence).  Usage: check_invariants.py EN.tex JA.tex"""
import collections, re, sys
ws = lambda s: re.sub(r"\s+", " ", s).strip()


def strip_comments(t): return re.sub(r"(?<!\\)%.*", "", t)


def extract(t):
    t = strip_comments(t); d = {}
    envs = r"equation\*?|align\*?|aligned|gather\*?|multline\*?|cases|array|split|alignat\*?"
    disp = [ws(m.group(0)) for m in re.finditer(r"\\\[.*?\\\]|\\begin\{(%s)\}.*?\\end\{\1\}" % envs, t, re.S)]
    d["display"] = disp
    t2 = re.sub(r"\\\[.*?\\\]|\\begin\{(%s)\}.*?\\end\{\1\}" % envs, " ", t, flags=re.S)
    d["inline"] = collections.Counter(ws(m.group(0)) for m in re.finditer(r"(?<!\\)\$(?:[^$\\]|\\.)*?\$", t2, re.S))
    for name, pat in (("label", r"\\label\{[^}]*\}"), ("ref", r"\\(?:eq)?ref\{[^}]*\}"), ("cite", r"\\cite[a-z]*\*?(?:\[[^\]]*\])*\{[^}]*\}"),
                      ("href_url", r"\\href\{[^}]*\}"), ("url", r"\\url\{[^}]*\}"), ("path", r"\\path\{[^}]*\}"), ("texttt", r"\\texttt\{[^}]*\}"),
                      ("graphics", r"\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}"), ("input", r"\\input\{[^}]*\}"),
                      ("begin_end", r"\\(?:begin|end)\{[a-zA-Z*]+\}")):
        d[name] = collections.Counter(ws(m.group(0)) for m in re.finditer(pat, t))
    d["numbers"] = collections.Counter(re.findall(r"(?<![A-Za-z\\{_^])\d[\d,]*(?:\.\d+)?", re.sub(r"(?<!\\)\$(?:[^$\\]|\\.)*?\$", " ", t2)))
    return d


a, b = extract(open(sys.argv[1], encoding="utf-8").read()), extract(open(sys.argv[2], encoding="utf-8").read()); bad = 0
if a["display"] != b["display"]:
    bad += 1; print("DISPLAY formulas differ: %d vs %d" % (len(a["display"]), len(b["display"])))
    for i, (x, y) in enumerate(zip(a["display"], b["display"])):
        if x != y: print("  first difference at #%d:\n   EN: %s\n   JA: %s" % (i, x[:300], y[:300])); break
for k in a:
    if k == "display": continue
    if a[k] != b[k]:
        miss = a[k] - b[k]; extra = b[k] - a[k]
        if k != "numbers": bad += 1
        print("%s differ: missing in JA %d, extra in JA %d" % (k.upper(), sum(miss.values()), sum(extra.values())))
        for x, n in list(miss.items())[:8]: print("   missing x%d: %s" % (n, x[:160]))
        for x, n in list(extra.items())[:8]: print("   extra   x%d: %s" % (n, x[:160]))
print("%s: display %d, inline %d, labels %d, refs %d, cites %d -> %s" % (sys.argv[2].split("/")[-1], len(a["display"]), sum(a["inline"].values()), sum(a["label"].values()),
      sum(a["ref"].values()), sum(a["cite"].values()), "OK" if bad == 0 else "%d KIND(S) DIFFER" % bad))
sys.exit(1 if bad else 0)
