"""python -m geoenclosereader {tree|verify|selftest} ...

  tree    LEDGER_GLOB                       structural check of every tree file
  verify  LEDGER_GLOB PLAN.json OUT.jsonl [--procs N]
  selftest                                  quick regression against audited values (about 2 min)
"""
import sys, json, multiprocessing as mp
from . import ledger as L, verify as V, __version__


def main(argv):
    if not argv or argv[0] in ("-h", "--help"): print(__doc__); return 0
    cmd = argv[0]
    if cmd == "tree":
        import glob; bad = 0
        for fn in sorted(glob.glob(argv[1])):
            r = L.check_tree(L.read(fn)); bad += not r["ok"]; print(json.dumps({"file": fn.split('/')[-1], **r}))
        return 1 if bad else 0
    if cmd == "verify":
        rows = L.read_many(argv[1]); plan = json.load(open(argv[2])); procs = int(argv[argv.index("--procs")+1]) if "--procs" in argv else 1
        items = [(r, plan) for r in V.select(rows, plan)]; n_ok = 0
        with open(argv[3], "w") as out, mp.Pool(procs) as pool:
            for res in pool.imap(V.run_item, items):
                res["reader_version"] = __version__; n_ok += res["confirmed"]
                out.write(json.dumps(res) + "\n"); out.flush()
                print(res["leaf"], res["quantity"], "confirmed" if res["confirmed"] else "NOT confirmed", res["grid_used"], res["seconds"], flush=True)
        print(f"{n_ok}/{len(items)} confirmed"); return 0 if n_ok == len(items) else 1
    if cmd == "selftest":
        from .selftest import run; return run()
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
