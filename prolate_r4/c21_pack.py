"""Reproducible C21 pilot package: sources, logs, JSON, reports, SHA256SUMS.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
import hashlib,json,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/"runs/2026-11-18/D_PRO_C21_H_PILOT"
PIN="fdfb498f2117cc0c5d72e88cc3be05eac9727bd8"
R3=Path("/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source/prolate_r1")
GIT=Path("/home/daybreak/bg-spheroid-family")
R3FILES=("__init__.py","api.py","center_bounds.py","density.py",
         "jets.py","intervals.py","quadrature.py")
def sha(b):return hashlib.sha256(b).hexdigest()
def filehash(path):return sha(Path(path).read_bytes())
def build():
 pins=["# R3 exact source-pin check","Status: DIAGNOSTIC_ONLY / NOT_EVIDENCE",
       "commit: "+PIN,""]
 for name in R3FILES:
  local=(R3/name).read_bytes()
  upstream=subprocess.check_output(["git","-C",str(GIT),"show",PIN+":prolate_r1/"+name])
  if local!=upstream:raise RuntimeError("R3 pin mismatch "+name)
  pins.append(sha(local)+"  prolate_r1/"+name)
 (RUN/"R3_PIN_CHECK.md").write_text("\n".join(pins)+"\n")
 sources=sorted(ROOT.glob("prolate_r4/c21_*.py"))
 sources += [ROOT/"prolate_r4/test_c21_rho2.py",
             ROOT/"prolate_r4/ANALYSIS_C21.md"]
 assert all(p.exists() for p in sources)
 docs=sorted(p for p in RUN.iterdir() if p.is_file() and
         p.name not in ("SHA256SUMS","ZIP_SHA256.txt","C21_H_PILOT_20261118.zip"))
 files=sorted(sources+docs,key=lambda x:x.relative_to(ROOT).as_posix())
 for p in files:
  if not p.resolve().is_relative_to(ROOT):raise RuntimeError("bad path")
 manifest="".join(f"{filehash(p)}  {p.relative_to(ROOT).as_posix()}\n" for p in files)
 (RUN/"SHA256SUMS").write_text(manifest)
 to_zip=files+[RUN/"SHA256SUMS"]
 zpath=RUN/"C21_H_PILOT_20261118.zip"
 with zipfile.ZipFile(zpath,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in to_zip:
   info=zipfile.ZipInfo(p.relative_to(ROOT).as_posix(),date_time=(2026,11,18,0,0,0))
   info.compress_type=zipfile.ZIP_DEFLATED
   info.external_attr=(0o100644 << 16)
   z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None
  for p in to_zip:assert z.read(p.relative_to(ROOT).as_posix())==p.read_bytes()
 zipsha=filehash(zpath)
 (RUN/"ZIP_SHA256.txt").write_text(zipsha+"  "+zpath.name+"\n")
 print(json.dumps({"status":"DIAGNOSTIC_ONLY / NOT_EVIDENCE",
   "files_in_zip":len(to_zip),"r3_pin_files_verified":len(R3FILES),
   "zip_sha256":zipsha,"bytes":zpath.stat().st_size,
   "zip_member_bytewise_check":"PASS"},indent=2))
if __name__=="__main__":build()
