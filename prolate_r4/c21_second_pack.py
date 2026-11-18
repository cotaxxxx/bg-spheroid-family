"""SHA256 and ZIP checkpoint of second-order C21 H diagnostics.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. No background completion claim.
"""
from pathlib import Path
import hashlib,json,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"runs/2026-11-18/D_PRO_C21_H_SECOND_ORDER"
R3=Path("/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source/prolate_r1")
GIT=Path("/home/daybreak/bg-spheroid-family")
PIN="fdfb498f2117cc0c5d72e88cc3be05eac9727bd8"
R3FILES=("__init__.py","api.py","center_bounds.py","density.py",
         "jets.py","intervals.py","quadrature.py")
ZIP_NAME="D_PRO_C21_H_SECOND_ORDER_DIAGNOSTIC_20261118.zip"
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
def sha(b):return hashlib.sha256(b).hexdigest()
def run():
 lines=["# Pinned R3 original source; DIAGNOSTIC_ONLY / NOT_EVIDENCE","pin: "+PIN,""]
 for name in R3FILES:
  b=(R3/name).read_bytes()
  original=subprocess.check_output(["git","-C",str(GIT),"show",PIN+":prolate_r1/"+name])
  assert b==original,("frozen R3 SHA mismatch",name)
  lines.append(sha(b)+"  prolate_r1/"+name)
 (OUT/"R3_PIN_CHECK.md").write_text("\n".join(lines)+"\n")
 sources=list(ROOT.glob("prolate_r4/c21_second_*.py"))
 sources.append(ROOT/"prolate_r4/ANALYSIS_C21_SECOND_ORDER.md")
 filenames=sources[:]
 for p in OUT.rglob("*"):
  if not p.is_file():continue
  if p.name in ("SHA256SUMS","ZIP_SHA256.txt","pack_result.log",ZIP_NAME):continue
  if p.name.endswith(".tmp") or p.name.endswith(".pyc"):continue
  filenames.append(p)
 names=sorted(set(filenames),key=lambda p:p.relative_to(ROOT).as_posix())
 assert all(p.resolve().is_relative_to(ROOT) for p in names)
 (OUT/"SHA256SUMS").write_text("".join(
   sha(p.read_bytes())+"  "+p.relative_to(ROOT).as_posix()+"\n"
   for p in names))
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
 ziphash=sha(zpath.read_bytes())
 (OUT/"ZIP_SHA256.txt").write_text(ziphash+"  "+ZIP_NAME+"\n")
 print(json.dumps({"status":STATUS,"zip":str(zpath.relative_to(ROOT)),
  "zip_sha256":ziphash,"zip_members":len(names)+1,
  "SHA256SUMS_entries":len(names),
  "R3_original_files_bytewise_verified":len(R3FILES),
  "CRC_and_zip_member_bytes_match":True},indent=2))
if __name__=="__main__":run()
