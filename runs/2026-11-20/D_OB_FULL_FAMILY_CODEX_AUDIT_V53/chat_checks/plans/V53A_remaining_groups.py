"""Amendment V53-A (fixed before run). DIAGNOSTIC_ONLY / NOT_EVIDENCE.
V53 was stopped by chat after 49 items (all confirmed; kept as V53_results_part1.jsonl / V53_run_STOPPED.log): the
coarse leaves of leaves/21H-31H took 4-8 minutes each, so the full plan (about 220 items) would have needed many hours
next to the running reproduction. Groups already finished (low_H, finer_H, window_H, 15 each) are not repeated.
Remaining groups, new seed 531, same kernels, ladders, depths and claims as V53:
  leaves_H_21_31: 3 weakest + 3 random (the 4 already done are excluded from the pool)
  thin_H, mixed_H, recovered_H, mixed_X, recovered_X, rim_X: 2 weakest + 2 random each
  salvage_H: all 8
  leaves_V, finer_V, low_V, leaves_Z, finer_Z, low_Z: 3 weakest + 3 random each
"""
import sys, json, random, multiprocessing as mp, importlib.util
spec = importlib.util.spec_from_file_location("V53", "plans/V53_oblate_full_family.py"); P = importlib.util.module_from_spec(spec); sys.modules["V53"] = P; spec.loader.exec_module(P)

if __name__ == '__main__':
    root, done_path, out = sys.argv[1], sys.argv[2], sys.argv[3]; rng = random.Random(531); items = []
    done = {json.loads(l)["leaf"] for l in open(done_path)}
    key = lambda r: r["file"].split('/')[-2] + "/" + r["file"].split('/')[-1] + ":" + r["path"]
    G = [("leaves_H_21_31", "leaves/[23][0-9]H.tsv", "H", 3, 3), ("thin_H", "thin/*H.tsv", "H", 2, 2), ("mixed_H", "mixed/*H.tsv", "H", 2, 2),
         ("recovered_H", "recovered/*H.tsv", "H", 2, 2), ("mixed_X", "mixed/*H.tsv", "X", 2, 2), ("recovered_X", "recovered/*H.tsv", "X", 2, 2),
         ("rim_X", "rim.tsv", "X", 2, 2), ("leaves_V", "leaves/*V.tsv", "V", 3, 3), ("finer_V", "finer/*V.tsv", "V", 3, 3), ("low_V", "low/*V.tsv", "V", 3, 3),
         ("leaves_Z", "leaves/*Z.tsv", "Z", 3, 3), ("finer_Z", "finer/*Z.tsv", "Z", 3, 3), ("low_Z", "low/*Z.tsv", "Z", 3, 3)]
    for g, pat, mode, nw, nr in G:
        rs = [r for r in P.rows(f"{root}/{pat}", {mode}) if key(r) not in done]
        if g == "leaves_H_21_31": rs = [r for r in rs if 21 <= int(r["file"].split('/')[-1][:2]) <= 31]
        items += [(g, r) for r in P.pick(rs, rng, nw, nr)]
    items += [("salvage_H", r) for r in P.rows(f"{root}/salvage/*H.tsv", {"H"})]
    n = ok = 0
    with open(out, "w") as f, mp.Pool(2) as pool:
        for r in pool.imap(P.run, items):
            n += 1; ok += r["confirmed"]; f.write(json.dumps(r) + "\n"); f.flush()
            print(r["group"], r["leaf"], r["confirmed"], r["ladder"], r["extreme"], r["seconds"], flush=True)
    print(f"{ok}/{n} confirmed")
