#!/usr/bin/env python3
"""Read-only C21 checkpoint audit. Never imports or runs a numerical solver.

Usage: python verify_stopped_snapshot.py --run /absolute/existing/run \
         --output /absolute/new/audit.json
The output must be a new file outside the referenced run directory.
"""
from __future__ import annotations
import argparse
import collections
import datetime as dt
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import re
import sys

PLATE = ["79/16", "5"]
SPECIAL = "R63_T63"
MIN = F(1, 256)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def rect(node):
    return tuple(F(str(v)) for key in ("R", "tau") for v in node[key])


def area(node):
    a,b,c,d = rect(node)
    return (b-a)*(d-c)


class Audit:
    def __init__(self, run):
        self.run = run
        self.errors = []
        self.inputs = {}

    def check(self, ok, message):
        if not ok:
            self.errors.append(message)
        return bool(ok)

    def load(self, relative):
        path = (self.run / relative).resolve()
        if not path.is_relative_to(self.run):
            raise ValueError("Input escapes run: " + str(relative))
        data = path.read_bytes()
        record = {"relative_path": str(path.relative_to(self.run)), "sha256": digest(data), "bytes": len(data)}
        self.inputs[str(path)] = record
        return json.loads(data), record

    def expected(self, name, roots):
        if not re.fullmatch(r"R\d{2}_T\d{2}(?:\.(?:R|tau)[01])*", name):
            raise ValueError("Invalid node ID: " + name)
        parts = name.split(".")
        out = {k:v for k,v in roots[parts[0]].items() if k != "route"}
        for token in parts[1:]:
            a,b,c,d = rect(out)
            axis = "R" if b-a >= d-c else "tau"
            self.check(b-a > MIN or d-c > MIN, "Split below minimum: " + out["id"])
            self.check(token == axis+token[-1], "Wrong split axis: " + name)
            lo,hi = (a,b) if axis == "R" else (c,d)
            mid = (lo+hi)/2
            bounds = (lo,mid) if token[-1] == "0" else (mid,hi)
            out = {**out, "parent":out["id"], "id":out["id"]+"."+token,
                   "depth":out["depth"]+1, axis:list(map(str,bounds))}
        return out

    def execute(self):
        st, _ = self.load("STATE.json")
        summary, _ = self.load("SUMMARY.json")
        registry, _ = self.load("REGISTRY.json")
        self.check(st["schema"] == "heavy_slab_v1" and st["plate"] == PLATE, "State schema/plate mismatch")
        self.check(registry["plate"] == PLATE and registry["global_wall_cap_seconds"] == 129600, "Registry plate/cap mismatch")
        self.check(st["workers"] == 12 and st["global_36h_cap_s"] == 129600, "State workers/cap mismatch")
        self.check(st["status"] == registry["status"] and st["no_cover_certification"] is True, "Diagnostic status mismatch")
        self.check(registry["min_edge"] == "1/256" and registry["max_workers"] == 12, "Registry minimum/workers mismatch")
        roots = {n["id"]:n for n in registry["roots"]}
        rootnames = {f"R{i:02d}_T{j:02d}" for i in range(64) for j in range(64)}
        self.check(len(registry["roots"]) == 4096 and set(roots) == rootnames, "Root IDs/count mismatch")
        self.check({n["rank"] for n in roots.values()} == set(range(4096)), "Root ranks not a permutation")
        for name,node in roots.items():
            i,j = int(name[1:3]),int(name[5:7])
            self.check(rect(node) == (F(i,64),F(i+1,64),F(j,64),F(j+1,64)), "Root rectangle: "+name)
            self.check(node["root"] == name and node["parent"] is None and node["depth"] == 0, "Root metadata: "+name)
        active = [t["node"] for t in st["terminal"]]+st["pending"]+st["inflight"]
        ids = [n["id"] for n in active]
        self.check(len(ids) == len(set(ids)), "Duplicate active node")
        byroot = collections.defaultdict(F)
        for node in active:
            self.check(node == self.expected(node["id"],roots), "Active geometry/metadata: "+node["id"])
            byroot[node["root"]] += area(node)
        self.check(all(byroot[n] == F(1,4096) for n in roots), "Root leaf area partition mismatch")
        splitmap = {s["id"]:s for s in st["splits"]}
        self.check(len(splitmap) == len(st["splits"]) and not set(splitmap).intersection(ids), "Duplicate/active split parent")
        children = []
        for name,item in splitmap.items():
            node = self.expected(name,roots)
            a,b,c,d = rect(node)
            axis = "R" if b-a >= d-c else "tau"
            expected = [name+"."+axis+str(i) for i in (0,1)]
            self.check(item["axis"] == axis and item["children"] == expected, "Split children/axis: "+name)
            self.check(F(item["area"]) == area(node) and item["depth"] == node["depth"] and item["zero_membership_record"] is True, "Split metadata: "+name)
            children.extend(item["children"])
        self.check(len(children) == len(set(children)), "Repeated child in split tree")
        self.check(set(roots)|set(children) == set(ids)|set(splitmap), "Tree cover is incomplete or has extra nodes")
        terminals = {t["node"]["id"]:t for t in st["terminal"]}
        processed = {p["id"]:p for p in st["processed"]}
        self.check(len(processed) == len(st["processed"]), "Repeated processed ID")
        self.check(set(processed) == set(terminals)|set(splitmap), "Processed/tree IDs mismatch")
        signs = collections.Counter()
        positive = []
        remaining = []
        box_evidence = []
        categories = collections.Counter()
        category_area = collections.defaultdict(F)
        dist = collections.Counter()
        distarea = collections.defaultdict(F)

        def classify(category,node,route=None,interval=None):
            a,b,c,d = rect(node)
            ar = area(node)
            categories[category] += 1
            category_area[category] += ar
            key = (category,node["depth"],str(b-a),str(d-c))
            dist[key] += 1
            distarea[key] += ar
            if category not in ("decided_positive","decided_negative"):
                remaining.append({"category":category,"id":node["id"],"R":node["R"],"tau":node["tau"],
                                  "lambda":PLATE,"depth":node["depth"],"R_width":str(b-a),"tau_width":str(d-c),
                                  "area_exact":str(ar),"route":route,"H_interval":interval})

        for name,item in processed.items():
            try:
                node = self.expected(name,roots)
                self.check(item["R"] == node["R"] and item["tau"] == node["tau"] and item["depth"] == node["depth"] and F(item["area"]) == area(node), "Processed geometry: "+name)
                terminal = terminals.get(name)
                if terminal:
                    relative = terminal["source_json"]
                    self.check(relative == "boxes/"+name+".json", "Unexpected source JSON path: "+name)
                    self.check(terminal["route"] == item["route"], "Terminal route differs: "+name)
                else:
                    relative = "boxes/"+name+".json"
                    self.check(splitmap[name]["route"] == item["route"], "Split route differs: "+name)
                box, manifest = self.load(relative)
                inp = box["input_box"]
                self.check(box["id"] == name and box["status"] == st["status"], "JSON ID/status: "+name)
                self.check(inp["R"] == node["R"] and inp["tau"] == node["tau"] and inp["lambda"] == PLATE, "JSON input box: "+name)
                route = box.get("route_from_position") if item["status"] == "EVALUATED" else box.get("route")
                self.check(route == item["route"], "JSON route: "+name)
                evidence = {"id":name,"processed_status":item["status"],"route":route,**manifest}
                if item["status"] == "OPEN":
                    self.check(terminal is not None and terminal["kind"] == "TUBE_OPEN_ERROR", "OPEN not terminal error: "+name)
                    self.check(box["H_interval"] is None, "OPEN has H interval: "+name)
                    if terminal:
                        self.check(box["reason"] == terminal["reason"], "OPEN reason differs: "+name)
                        category = "special_open_R63_T63" if name == SPECIAL else "other_open"
                        if name == SPECIAL:
                            self.check(node["depth"] == 0 and area(node) == F(1,4096), "Special corner geometry differs")
                        classify(category,node,route)
                    signs["OPEN"] += 1
                    evidence["H_interval"] = None
                else:
                    self.check(item["status"] == "EVALUATED", "Unknown processed status: "+name)
                    interval = box["H_interval"]
                    lo,hi = F(str(interval["lower"])),F(str(interval["upper"]))
                    self.check(lo <= hi, "Reversed H interval: "+name)
                    sign = "positive" if lo > 0 else "negative" if hi < 0 else "contains_zero"
                    signs[sign] += 1
                    evidence.update(H_interval=interval,sign=sign)
                    if lo > 0:
                        positive.append({"id":name,"input_box":inp,"route":route,"H_interval":interval,
                                         "lower_exact":str(lo),"upper_exact":str(hi),"state_location":"terminal" if terminal else "split",
                                         "terminal_kind":terminal["kind"] if terminal else None,**manifest})
                    if terminal:
                        ti = terminal["H_interval"]
                        self.check((F(str(ti["lower"])),F(str(ti["upper"]))) == (lo,hi), "STATE/JSON H interval differs: "+name)
                        a,b,c,d = rect(node)
                        if terminal["kind"] == "DECIDED_NONZERO":
                            self.check(sign in ("positive","negative"), "Nonzero terminal contains zero: "+name)
                            classify("decided_"+sign,node,route,interval)
                        elif terminal["kind"] == "TUBE_MIN":
                            self.check(lo <= 0 <= hi and b-a <= MIN and d-c <= MIN, "Invalid minimum tube: "+name)
                            classify("tube_min",node,route,interval)
                        else:
                            self.check(False,"Unexpected evaluated terminal kind: "+name)
                    else:
                        a,b,c,d = rect(node)
                        self.check(lo <= 0 <= hi and (b-a > MIN or d-c > MIN), "Invalid zero split decision: "+name)
                box_evidence.append(evidence)
            except Exception as exc:
                self.errors.append("Processed JSON "+name+": "+type(exc).__name__+": "+str(exc))

        for node in st["pending"]:
            classify("pending",node)
        for node in st["inflight"]:
            classify("inflight",node)
        decided = [t for t in st["terminal"] if t["kind"] == "DECIDED_NONZERO"]
        tubes = [t for t in st["terminal"] if t["kind"] != "DECIDED_NONZERO"]
        ad = sum((area(t["node"]) for t in decided),F(0))
        at = sum((area(t["node"]) for t in tubes),F(0))
        ap = sum((area(n) for n in st["pending"]),F(0))
        ai = sum((area(n) for n in st["inflight"]),F(0))
        self.check(ad+at+ap+ai == 1, "Total exact normalized area is not 1")
        self.check(sum(category_area.values(),F(0)) == 1, "Classified active area is incomplete")
        expected_summary = {
            "attempted_terminal_or_split_nodes":len(st["processed"]),"split_parent_count":len(st["splits"]),
            "evaluated_complete_nodes":sum(p["status"] == "EVALUATED" for p in st["processed"]),
            "failed_OPEN_nodes":sum(p["status"] == "OPEN" for p in st["processed"]),
            "decided_count":len(decided),"tube_evaluated_count":len(tubes),
            "pending_unprocessed_count":len(st["pending"])+len(st["inflight"]),
            "decided_area_exact":str(ad),"tube_area_exact":str(at),"pending_area_exact":str(ap+ai),
            "area_total_exact":"1","area_partition_valid":True,"full_plate_done":not(st["pending"] or st["inflight"]),
            "elapsed_wall_cumulative_s":st["wall_elapsed_cumulative_s"],"never_a_mathematical_certificate":True}
        for key,value in expected_summary.items():
            self.check(summary.get(key) == value,"SUMMARY differs from STATE: "+key)
        special = None
        if SPECIAL in terminals and terminals[SPECIAL]["kind"] == "TUBE_OPEN_ERROR":
            special, special_manifest = self.load("CORNER_SPECIAL_RESERVED.json")
            special = {"raw_record":special,**special_manifest,"state_kind_preserved":"TUBE_OPEN_ERROR"}
        for name in ("PRE_RUN_FREEZE.md","RESUME_CONTINUOUS.log"):
            path = self.run/name
            if path.exists():
                data = path.read_bytes()
                self.inputs[str(path.resolve())] = {"relative_path":name,"sha256":digest(data),"bytes":len(data)}
        for path,record in self.inputs.items():
            self.check(digest(Path(path).read_bytes()) == record["sha256"],"Input changed during audit: "+record["relative_path"])
        return {
            "audit_status":"PASS" if not self.errors else "FAIL","errors":self.errors,
            "scope":"Checkpoint ledger, exact parameter-box partition, and recorded JSON consistency; no H/W recomputation and no mathematical certification.",
            "run":str(self.run),"plate_lambda":PLATE,"lambda_width_exact":"1/16",
            "normal_process_completion_claimed":False,"process_status_not_inspected":True,
            "checkpoint":{"completed_batches":st["completed_batches"],"inflight_count":len(st["inflight"]),
                          "settled_checkpoint":not st["inflight"],"sessions":st["sessions"],
                          "wall_elapsed_cumulative_s":st["wall_elapsed_cumulative_s"],
                          "clock_note":"The original runner updates this total only when a session returns normally; it does not include a paused in-progress session."},
            "counts":{"roots":len(roots),"splits":len(splitmap),"active_leaves":len(active),"processed":len(processed),
                      "processed_jsons_read":len(box_evidence),"recorded_H_signs":dict(signs)},
            "exact_area":{"decided":str(ad),"tube":str(at),"pending":str(ap),"inflight":str(ai),"total":str(ad+at+ap+ai),
                          "per_root_expected":"1/4096","normalization":"R-tau unit square"},
            "positive_H_count":len(positive),"positive_H_records":positive,
            "positive_scope_note":"All processed JSONs were inspected. Pending/inflight JSONs outside processed are not claimed as settled results.",
            "categories":[{"category":k,"count":categories[k],"area_exact":str(category_area[k])} for k in sorted(categories)],
            "distribution":[{"category":k[0],"depth":k[1],"R_width":k[2],"tau_width":k[3],"count":dist[k],"area_exact":str(distarea[k])} for k in sorted(dist)],
            "remaining_boxes":remaining,"special_corner_record":special,
            "processed_json_evidence":box_evidence,"input_manifest":list(self.inputs.values())}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run",required=True)
    p.add_argument("--output",required=True)
    args = p.parse_args()
    run,output = Path(args.run),Path(args.output)
    if not run.is_absolute() or not output.is_absolute():
        p.error("--run and --output must be absolute paths")
    run,output = run.resolve(),output.resolve()
    if output.is_relative_to(run) or output.exists():
        p.error("--output must be a new file outside --run")
    audit = Audit(run)
    try:
        result = audit.execute()
    except Exception as exc:
        result = {"audit_status":"FAIL","errors":audit.errors+[type(exc).__name__+": "+str(exc)],
                  "run":str(run),"input_manifest":list(audit.inputs.values()),"normal_process_completion_claimed":False}
    result["audit_time_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    result["audit_script_sha256"] = digest(Path(__file__).read_bytes())
    output.parent.mkdir(parents=True,exist_ok=True)
    fd = os.open(output,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,"w") as f:
        json.dump(result,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n");f.flush();os.fsync(f.fileno())
    print(json.dumps({"audit_status":result["audit_status"],"positive_H_count":result.get("positive_H_count"),
                      "errors":result["errors"],"output":str(output)},ensure_ascii=False))
    return 0 if result["audit_status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
