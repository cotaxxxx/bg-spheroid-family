"""Reproducible ZIP, frozen R3 file SHA; per-checkpoint measured evidence.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
from pathlib import Path
import hashlib,json,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"runs/2026-11-18/D_PRO_C21_H_HEAVY_SLAB"
R3=Path("/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source/prolate_r1")
GIT=Path("/home/daybreak/bg-spheroid-family")
PIN="fdfb498f2117cc0c5d72e88cc3be05eac9727bd8"
R3FILES=("__init__.py","api.py","center_bounds.py","density.py",
  "jets.py","intervals.py","quadrature.py")
ZIP="D_PRO_C21_H_HEAVY_SLAB_DIAGNOSTIC_20261118.zip"
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
def sha(buf):return hashlib.sha256(buf).hexdigest()
def pack():
 proof=["# R3 original pin bytewise comparison",
        "DIAGNOSTIC_ONLY / NOT_EVIDENCE",
        "commit "+PIN,""]
 for n in R3FILES:
  b=(R3/n).read_bytes()
  pin=subprocess.check_output(["git","-C",str(GIT),"show",PIN+":prolate_r1/"+n])
  assert b==pin,("R3_PIN_CHANGED",n)
  proof.append(sha(b)+"  prolate_r1/"+n)
 (OUT/"R3_PIN_CHECK.md").write_text("\n".join(proof)+"\n")
 files=list(ROOT.glob("prolate_r4/c21_heavy_*.py"))
 for f in OUT.rglob("*"):
  if not f.is_file():continue
  if f.name in ("SHA256SUMS","ZIP_SHA256.txt","pack_result.log",ZIP):continue
  if f.name.endswith(".tmp") or f.name.endswith(".pyc"):continue
  files.append(f)
 files=sorted(set(files),key=lambda f:f.relative_to(ROOT).as_posix())
 assert all(x.resolve().is_relative_to(ROOT) for x in files)
 (OUT/"SHA256SUMS").write_text("".join(
   sha(f.read_bytes())+"  "+f.relative_to(ROOT).as_posix()+"\n" for f in files))
 zpath=OUT/ZIP
 with zipfile.ZipFile(zpath,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for f in files+[OUT/"SHA256SUMS"]:
   zi=zipfile.ZipInfo(f.relative_to(ROOT).as_posix(),date_time=(2026,11,18,0,0,0))
   zi.compress_type=zipfile.ZIP_DEFLATED
   zi.external_attr=0o100644<<16
   z.writestr(zi,f.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None
  for f in files+[OUT/"SHA256SUMS"]:
   assert z.read(f.relative_to(ROOT).as_posix())==f.read_bytes()
 h=sha(zpath.read_bytes())
 (OUT/"ZIP_SHA256.txt").write_text(h+"  "+ZIP+"\n")
 print(json.dumps({"status":STATUS,"zip":str(zpath.relative_to(ROOT)),
  "SHA256SUMS_entries":len(files),"ZIP_files":len(files)+1,
  "ZIP_SHA256":h,"R3_pinned_files":len(R3FILES),
  "member_bytes_verified":True},indent=2))
if __name__=="__main__":pack()
