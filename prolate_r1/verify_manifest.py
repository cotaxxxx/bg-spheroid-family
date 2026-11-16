"""DIAGNOSTIC_ONLY / NOT_EVIDENCE: verify source contents before Dig execution."""
import hashlib
from pathlib import Path

def main():
    root=Path(__file__).resolve().parents[1]
    manifest=root/"prolate_r1"/"SHA256SUMS"
    count=0
    for line in manifest.read_text().splitlines():
        if not line or line.startswith("#"): continue
        expected,name=line.split("  ",1)
        path=root/name
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=expected:
            raise SystemExit("FAIL SHA256 "+name)
        count+=1
    print("PASS source SHA256:",count,"DIAGNOSTIC_ONLY / NOT_EVIDENCE")

if __name__=="__main__": main()
