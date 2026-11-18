"""Deterministic checkpoint ZIP and pinned R3 SHA for H cost pilot.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
from pathlib import Path
import hashlib,json,zipfile,subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"runs/2026-11-18/D_PRO_C21_H_COST_TRIM"
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
R3=Path("/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source/prolate_r1")
SOURCE_GIT=Path("/home/daybreak/bg-spheroid-family")
PIN="fdfb498f2117cc0c5d72e88cc3be05eac9727bd8"
FILENAMES=("__init__.py","api.py","center_bounds.py","density.py",
           "jets.py","intervals.py","quadrature.py")
ZIP="D_PRO_C21_H_COST_TRIM_DIAGNOSTIC_20261118.zip"
def sha(b):return hashlib.sha256(b).hexdigest()
def run():
 lines=["# Fixed R3 source hash audit — DIAGNOSTIC_ONLY / NOT_EVIDENCE",
        "pinned commit: "+PIN,""]
 for name in FILENAMES:
  blob=(R3/name).read_bytes()
  original=subprocess.check_output(["git","-C",str(SOURCE_GIT),
                                    "show",PIN+":prolate_r1/"+name])
  assert blob==original,("R3_SOURCE_CHANGED",name)
  lines.append(sha(blob)+"  prolate_r1/"+name)
 (OUT/"R3_PIN_CHECK.md").write_text("\n".join(lines)+"\n")
 filenames=list(ROOT.glob("prolate_r4/c21_cost_*.py"))
 filenames.extend(p for p in OUT.rglob("*") if p.is_file() and p.name not in
                  ("SHA256SUMS","ZIP_SHA256.txt","pack_result.log",ZIP)
                  and not p.name.endswith(".tmp") and not p.name.endswith(".pyc"))
 paths=sorted(set(filenames),key=lambda p:p.relative_to(ROOT).as_posix())
 (OUT/"SHA256SUMS").write_text("".join(
   sha(p.read_bytes())+"  "+p.relative_to(ROOT).as_posix()+"\n" for p in paths))
 zpath=OUT/ZIP
 with zipfile.ZipFile(zpath,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in paths+[OUT/"SHA256SUMS"]:
   info=zipfile.ZipInfo(p.relative_to(ROOT).as_posix(),date_time=(2026,11,18,0,0,0))
   info.compress_type=zipfile.ZIP_DEFLATED
   info.external_attr=0o100644<<16
   z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None
  for p in paths+[OUT/"SHA256SUMS"]:
   assert z.read(p.relative_to(ROOT).as_posix())==p.read_bytes()
 ziphash=sha(zpath.read_bytes())
 (OUT/"ZIP_SHA256.txt").write_text(ziphash+"  "+ZIP+"\n")
 print(json.dumps({"status":STATUS,"zip":str(zpath.relative_to(ROOT)),
  "sha256":ziphash,"SHA256SUMS_entries":len(paths),
  "zip_files":len(paths)+1,"source_R3_verified":len(FILENAMES),
  "zip_member_bytes_checked":True},indent=2))
if __name__=="__main__":run()
