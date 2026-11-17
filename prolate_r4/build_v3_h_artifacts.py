"""Package complete D-PRO R4 v3 H diagnostic with deterministic SHA/ZIP.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Does not run mathematics.
"""
from pathlib import Path
import hashlib,json,subprocess,zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"runs/2026-11-18/D_PRO_R4_RATMODEL_V3_H_CHAT"
PIN="fdfb498f2117cc0c5d72e88cc3be05eac9727bd8"
SRC=Path("/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source")
REPO=Path("/home/daybreak/bg-spheroid-family")
FROZEN=("__init__.py","api.py","center_bounds.py","density.py",
        "jets.py","intervals.py","quadrature.py")
def sha(data):return hashlib.sha256(data).hexdigest()
pins=["# R3 read-only source SHA-256 pins","",
      "Pinned commit: "+PIN,"Status: DIAGNOSTIC_ONLY / NOT_EVIDENCE",""]
for f in FROZEN:
    local=(SRC/"prolate_r1"/f).read_bytes()
    frozen=subprocess.check_output(["git","-C",str(REPO),"show",f"{PIN}:prolate_r1/{f}"])
    assert local==frozen, f"R3 pin mismatch: {f}"
    pins.append(f"{sha(local)}  prolate_r1/{f}")
(OUT/"R3_SOURCE_PINS.md").write_text("\n".join(pins)+"\n")
files=[*(ROOT/"prolate_r4"/p for p in (
    "ANALYSIS_V3_H.md","h_box2.py","verify_h_box2.py",
    "test_h_kernel.py","v35_w_split_preflight.py",
    "v35_w_b4_cover.py","build_v3_h_artifacts.py")),
  *(OUT/p for p in ("README.md","RUN_RECEIPT.md",
      "STAGE1_W_RULE_FREEZE.md","R3_SOURCE_PINS.md",
      "H_box2.json","H_box2.log","H_initial_failed.log",
      "checker.json","h_kernel_crosschecks.json",
      "W_stage1_4child_point_preflight.json",
      "W_stage1_4child_point_preflight.log",
      "W_stage1_4child_B4_cover.json",
      "W_stage1_4child_B4_cover.log"))]
assert all(p.is_file() and p.resolve().is_relative_to(ROOT) for p in files)
files.sort(key=lambda p:str(p.relative_to(ROOT)))
manifest="".join(f"{sha(p.read_bytes())}  {p.relative_to(ROOT)}\n" for p in files)
(OUT/"SHA256SUMS").write_text(manifest)
zip_path=OUT/"D_PRO_R4_V3_H_BOX2_DIAGNOSTIC_20261118.zip"
# Fixed timestamps and canonical member order for reproducible packaging.
with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files+[OUT/"SHA256SUMS"]:
        rel=str(p.relative_to(ROOT))
        info=zipfile.ZipInfo(rel,date_time=(2026,11,18,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=(0o100644 <<16)
        z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None
    for p in files+[OUT/"SHA256SUMS"]:
        assert z.read(str(p.relative_to(ROOT)))==p.read_bytes()
(OUT/"ZIP_SHA256.txt").write_text(
    sha(zip_path.read_bytes())+"  "+zip_path.name+"\n")
print(json.dumps({"status":"DIAGNOSTIC_ONLY / NOT_EVIDENCE",
                  "file_count_with_manifest":len(files)+1,
                  "zip_sha256":sha(zip_path.read_bytes()),
                  "zip_bytes":zip_path.stat().st_size,
                  "all_r3_pins_match":True,
                  "all_zip_contents_match":True},indent=2))
