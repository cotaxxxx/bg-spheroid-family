"""Fixed 27-box W1 Taylor-order/cell-count diagnostic sweep.

No sign-based selection, no CERTIFIED verdict, no modifications to source boxes.
Only 128-bit comparisons: original 128/192-bit baseline is separately sealed.
Run from repository root with a dedicated Python 3.11 virtualenv.
"""
import argparse
import concurrent.futures
import csv
import datetime
import hashlib
import json
import os
import pathlib
import resource
import statistics
import time
import traceback
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
STATUS = "DIAGNOSTIC_ONLY / NOT_EVIDENCE"
CELLS = {2048: (32,64), 8192: (64,128)}
ORDERS = (2,4,6)
SOURCE_FILES = ("kernel.py","kernel_w1.py","sweep_w1.py","boxes.json")
PLAN = HERE / "W1_SWEEP_PLAN.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_plan():
    data=json.loads(PLAN.read_text())
    assert data["status"]==STATUS
    assert data["precision_bits"]==128
    assert data["orders"]==list(ORDERS)
    assert data["cell_counts"]==list(CELLS)
    assert data["boxes"]==list(range(27))
    for name in SOURCE_FILES:
        if sha(HERE/name)!=data["source_sha256"][name]:
            raise RuntimeError("SOURCE_SHA_MISMATCH: "+name)
    return data


def perform_one(task):
    """Worker: fresh process context and one box/order/cell case."""
    boxid,order,ncells,box,prec=task
    start=time.perf_counter_ns()
    try:
        from flint import fmpq,arb
        from . import kernel_w1
        edges=lambda field: tuple(fmpq(x) for x in box[field])
        res=kernel_w1.V_box_details(edges("R"),edges("tau"),edges("lam"),
                                    prec,order,CELLS[ncells])
        # Exact dyadic endpoints; ONLY width is saved, never a sign.
        a=res.enclosure.lower().fmpq()
        b=res.enclosure.upper().fmpq()
        w=b-a
        if w<0:
            raise ArithmeticError("negative width")
        return {"box_id":boxid,"order":order,"requested_cells":ncells,
                "precision_bits":prec,"outcome":"computed",
                "enclosure_width_dyadic":str(w),
                "cells":res.cells,
                "density_evaluations":res.density_evaluations,
                "route":res.route,
                "wall_ns":time.perf_counter_ns()-start,
                "max_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                "status":STATUS}
    except BaseException:
        return {"box_id":boxid,"order":order,"requested_cells":ncells,
                "precision_bits":prec,"outcome":"ERROR",
                "traceback":traceback.format_exc(),
                "wall_ns":time.perf_counter_ns()-start,
                "max_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                "status":STATUS}


def prepare(tasks, out, plan):
    out.mkdir(parents=True,exist_ok=False)
    (out/"plan_used.json").write_text(json.dumps(plan,indent=2,ensure_ascii=False)+"\n")
    (out/"tasks_fixed.json").write_text(json.dumps([
        {"box_id":i,"order":order,"cells":n,"precision_bits":128}
        for i,order,n,_,_ in tasks],indent=2)+"\n")


def prepare_tasks(args):
    b=json.loads((HERE/"boxes.json").read_text())["boxes"]
    assert len(b)==27
    bmap={x["id"]:x for x in b}
    assert set(bmap)==set(range(27))
    return [(i,order,n,bmap[i],args.bits)
            for i in range(27)
            for order in args.orders for n in args.cells]


def summarize(rows):
    ans=[]
    for order in ORDERS:
        for n in CELLS:
            sub=[r for r in rows if r["order"]==order and r["requested_cells"]==n]
            success=[r for r in sub if r["outcome"]=="computed"]
            widths=[Fraction(r["enclosure_width_dyadic"]) for r in success]
            times=[r["wall_ns"] for r in success]
            ans.append({
                "order":order,"cells":n,
                "computed":len(success),"expected":27,
                "width_mean_dyadic":str(sum(widths,Fraction(0))/len(widths)) if widths else "",
                "width_mean_decimal":format(float(sum(widths,Fraction(0))/len(widths)),".9g") if widths else "",
                "width_median_decimal":format(float(statistics.median(widths)),".9g") if widths else "",
                "width_max_decimal":format(float(max(widths)),".9g") if widths else "",
                "worker_wall_mean_s":format(sum(times)/len(times)/1e9,".6f") if times else "",
                "worker_wall_max_s":format(max(times)/1e9,".6f") if times else "",
                "max_rss_kib":max((r["max_rss_kib"] for r in sub),default=0),
                "status":STATUS})
    return ans


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",required=True)
    p.add_argument("--orders",default="2,4,6")
    p.add_argument("--cells",default="2048,8192")
    p.add_argument("--bits",type=int,default=128)
    p.add_argument("--workers",type=int,default=6)
    args=p.parse_args()
    args.orders=tuple(int(x) for x in args.orders.split(","))
    args.cells=tuple(int(x) for x in args.cells.split(","))
    if args.orders!=ORDERS or args.cells!=tuple(CELLS) or args.bits!=128:
        raise SystemExit("WRONG_FIXED_SWEEP_PLAN")
    if not (1<=args.workers<=8):
        raise SystemExit("INVALID_WORKER_COUNT")
    plan=verify_plan()
    tasks=prepare_tasks(args)
    if len(tasks)!=162:
        raise RuntimeError("wrong task count")
    out=pathlib.Path(args.out)
    prepare(tasks,out,plan)
    start=time.perf_counter_ns()
    rows=[]
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        tasks_by_future={pool.submit(perform_one,t):t for t in tasks}
        for future in concurrent.futures.as_completed(tasks_by_future):
            row=future.result()
            rows.append(row)
            with (out/"results.partial.jsonl").open("a") as f:
                f.write(json.dumps(row,sort_keys=True,ensure_ascii=False)+"\n")
            if len(rows)%9==0 or row["outcome"]!="computed":
                print("PROGRESS",len(rows),"/162", "last=",row["box_id"],row["order"],row["requested_cells"],
                      "outcome=",row["outcome"],flush=True)
    total_ns=time.perf_counter_ns()-start
    rows.sort(key=lambda r:(r["box_id"],r["order"],r["requested_cells"]))
    summaries=summarize(rows)
    (out/"results.json").write_text(json.dumps({
        "status":STATUS,"elapsed_ns":total_ns,
        "workers":args.workers,"precision_bits":args.bits,"results":rows,
        "summary":summaries},indent=2,ensure_ascii=False)+"\n")
    fields=("box_id","order","requested_cells","precision_bits","outcome",
            "enclosure_width_dyadic","cells","density_evaluations","route",
            "wall_ns","max_rss_kib","status")
    with (out/"results.tsv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore",lineterminator="\n",delimiter="\t")
        w.writeheader()
        for row in rows:
            w.writerow(row)
    with (out/"summary.tsv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(summaries[0]),lineterminator="\n",delimiter="\t")
        w.writeheader()
        w.writerows(summaries)
    print("TOTAL_WORKER_CASES",len(rows),flush=True)
    print("ERRORS",sum(x["outcome"]!="computed" for x in rows),flush=True)
    print("TOTAL_WALL_S",format(total_ns/1e9,'.6f'),flush=True)
    for r in summaries:
        print("SUMMARY",r["order"],r["cells"],r["computed"],
              r["width_mean_decimal"],r["worker_wall_mean_s"],flush=True)
    print(STATUS,flush=True)
    if any(x["outcome"]!="computed" for x in rows):
        raise SystemExit(2)


if __name__=="__main__":
    main()
