"""Read-only byte verification of a delivered diagnostic research package."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def verify(root, manifest='SHA256SUMS'):
    root = root.resolve()
    checked = []
    for line in (root / manifest).read_text().splitlines():
        if not line.strip():
            continue
        expected, relative = line.split(maxsplit=1)
        relative = relative.strip()
        target = (root / relative).resolve()
        if root not in target.parents or not target.is_file():
            raise ValueError(f'Invalid manifest path: {relative}')
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f'Byte hash differs: {relative}')
        if relative in checked:
            raise ValueError(f'Duplicate manifest path: {relative}')
        checked.append(relative)
    return {'status': 'all_listed_bytes_match', 'file_count': len(checked), 'manifest': manifest}


if __name__ == '__main__':
    print(json.dumps(verify(ROOT)))
