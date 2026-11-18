"""SHA-256 evidence bundle for a *completed checkpoint*, not a future run.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
from pathlib import Path
import hashlib,json,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"runs/2026-11-18/D_PRO_C21_SLAB_ADAPTIVE"
R3=Path("/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source/prolate_r1")
GIT=Path("/home/daybreak/bg-spheroid-family")
PIN="fdfb498f2117cc0c5d72e88cc3be05eac9727bd8"
R3FILES=("__init__.py","api.py","center_bounds.py","density.py",
  "jets.py","intervals.py","quadrature.py")
ZIP_NAME="D_PRO_C21_H_SLAB_DIAGNOSTIC_CHECKPOINT_20261118.zip"
def sha(b):return hashlib.sha256(b).hexdigest()
def run():
 lines=["# Fixed R3 SHA pins. DIAGNOSTIC_ONLY / NOT_EVIDENCE",
   "commit: "+PIN,""]
 for name in R3FILES:
  b=(R3/name).read_bytes()
  g=subprocess.check_output(["git","-C",str(GIT),"show",PIN+":prolate_r1/"+name])
  assert b==g,("R3 immutable source SHA mismatch",name)
  lines.append(sha(b)+"  prolate_r1/"+name)
 (OUT/"R3_PIN_CHECK.md").write_text("\n".join(lines)+"\n")
 names=[]
 for p in ROOT.glob("prolate_r4/slab_*.py"):names.append(p)
 for p in OUT.rglob("*"):
  if not p.is_file() or p.name in ("SHA256SUMS","ZIP_SHA256.txt","pack_result.log",ZIP_NAME):continue
  if p.name.endswith(".tmp") or p.name.endswith(".pyc"):continue
  names.append(p)
 names.sort(key=lambda p:p.relative_to(ROOT).as_posix())
 assert all(p.resolve().is_relative_to(ROOT) for p in names)
 text="".join(sha(p.read_bytes())+"  "+p.relative_to(ROOT).as_posix()+"\n" for p in names)
 (OUT/"SHA256SUMS").write_text(text)
 zpath=OUT/ZIP_NAME
 with zipfile.ZipFile(zpath,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in names+[OUT/"SHA256SUMS"]:
   info=zipfile.ZipInfo(p.relative_to(ROOT).as_posix(),date_time=(2026,11,18,0,0,0))
   info.compress_type=zipfile.ZIP_DEFLATED
   info.external_attr=0o100644<<16
   z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None
  for p in names+[OUT/"SHA256SUMS"]:
   assert z.read(p.relative_to(ROOT).as_posix())==p.read_bytes()
 zip_sha=sha(zpath.read_bytes())
 (OUT/"ZIP_SHA256.txt").write_text(zip_sha+"  "+ZIP_NAME+"\n")
 print(json.dumps({"status":"DIAGNOSTIC_ONLY / NOT_EVIDENCE",
    "zip":str(zpath.relative_to(ROOT)),
    "zip_sha256":zip_sha,"zip_members":len(names)+1,
    "SHA256SUMS_entries":len(names),"frozen_R3_pins_verified":len(R3FILES),
    "zip_content_bytewise_check":True,
    "record_type":"PARTIAL_OR_FULL_CHECKPOINT_AS_LEDGER_SAYS"},indent=2))
if __name__=="__main__":run()
