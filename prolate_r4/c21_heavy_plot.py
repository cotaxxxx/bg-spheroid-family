"""SVG of evaluated terminal tubes only; pending is grey background.
DIAGNOSTIC_ONLY / NOT_EVIDENCE, no spatial sign interpolation.
"""
import html,json
from fractions import Fraction as F
from . import c21_heavy_cover as c
OUT=c.OUT;STATUS=c.STATUS
def f(x):return float(F(x))
def build():
 st=c.readstate()
 stat=c.counts(st)
 W=880;H=880;margin=90
 svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="1070" viewBox="0 0 1120 1070">',
   '<rect x="0" y="0" width="1120" height="1070" fill="#ffffff"/>',
   '<text x="90" y="42" font-family="sans-serif" font-weight="bold" font-size="22">D-PRO C21 heavy slab: evaluated terminal tubes</text>',
   '<text x="90" y="68" font-family="sans-serif" font-size="14">DIAGNOSTIC_ONLY / NOT_EVIDENCE; unsampled gray = PENDING_UNEVALUATED</text>',
   f'<rect x="{margin}" y="{margin}" width="{W}" height="{H}" fill="#e5e7eb" stroke="#374151" stroke-width="2"/>']
 for t in st["terminal"]:
  box=t["node"]
  r0,r1=map(f,box["R"]);t0,t1=map(f,box["tau"])
  x=margin+r0*W;y=margin+(1-t1)*H
  width=(r1-r0)*W;height=(t1-t0)*H
  color={"DECIDED_NONZERO":"#2563eb","TUBE_MIN":"#d97706",
         "TUBE_OPEN_ERROR":"#be123c"}[t["kind"]]
  svg.append(f'<rect x="{x:.9f}" y="{y:.9f}" width="{width:.9f}" height="{height:.9f}" fill="{color}" stroke="#ffffff" stroke-width=".3"><title>{html.escape(box["id"])}: {html.escape(t["kind"])}</title></rect>')
 for i in range(0,5):
  x=margin+i*W/4;y=margin+(4-i)*H/4
  svg.append(f'<line x1="{x}" x2="{x}" y1="{margin}" y2="{margin+H}" stroke="#cbd5e1" stroke-width=".4"/>')
  svg.append(f'<line x1="{margin}" x2="{margin+W}" y1="{y}" y2="{y}" stroke="#cbd5e1" stroke-width=".4"/>')
  svg.append(f'<text x="{x-3}" y="990" font-size="13" font-family="sans-serif">{i/4:.2f}</text>')
  svg.append(f'<text x="55" y="{y+4}" font-size="13" font-family="sans-serif">{i/4:.2f}</text>')
 svg.extend(['<text x="510" y="1020" font-size="17" font-family="sans-serif">R →</text>',
  '<text transform="translate(27,600) rotate(-90)" font-size="17" font-family="sans-serif">τ →</text>',
  f'<text x="90" y="1050" font-size="13" font-family="sans-serif">Measured tubes {stat["tube_evaluated_count"]}; decided {stat["decided_count"]}; pending {stat["pending_unprocessed_count"]}. Not a complete map.</text>',
  '</svg>'])
 (OUT/"TUBE_DISTRIBUTION.svg").write_text("\n".join(svg)+"\n")
 print(STATUS,"SVG rectangles",len(st["terminal"]))
if __name__=="__main__":build()
