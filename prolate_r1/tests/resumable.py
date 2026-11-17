"""DIAGNOSTIC_ONLY / NOT_EVIDENCE.
Durable per-case results. Fixed mathematical test functions are unchanged.
A killed in-progress case is retried from its beginning, not from an inner cell.
"""
import argparse
from contextlib import contextmanager, nullcontext, redirect_stdout, redirect_stderr
from datetime import datetime, timezone
import faulthandler
import hashlib
import json
import os
from pathlib import Path
import platform
import signal
import sys
from time import perf_counter_ns
import traceback
from uuid import uuid4

STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
SCHEMA="d-pro-r1-r2-cases-v1"

def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def sync_dir(path):
    if os.name=="posix":
        fd=os.open(str(path),os.O_RDONLY|getattr(os,"O_DIRECTORY",0))
        try: os.fsync(fd)
        finally: os.close(fd)

def atomic_json(path,value,create=False):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    if create and path.exists():
        raise FileExistsError("refusing to overwrite "+str(path))
    temp=path.with_name(path.name+".tmp-"+uuid4().hex)
    try:
        with temp.open("x",encoding="utf-8") as stream:
            stream.write(json.dumps(value,ensure_ascii=False,indent=2)+"\n")
            stream.flush(); os.fsync(stream.fileno())
        os.replace(temp,path)
        sync_dir(path.parent)
    finally:
        if temp.exists(): temp.unlink()

def read_json(path):
    with Path(path).open(encoding="utf-8") as stream:
        return json.load(stream)

@contextmanager
def exclusive_lock(path):
    # Advisory OS lock is automatically released after SIGKILL/process death.
    # No stale lock deletion, PID guessing, or concurrent snapshot writers.
    with Path(path).open("a+b") as stream:
        if os.name=="posix":
            import fcntl
            try: fcntl.flock(stream.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
            except OSError as exc:
                raise RuntimeError("another runner holds "+str(path)) from exc
            try: yield
            finally: fcntl.flock(stream.fileno(),fcntl.LOCK_UN)
        elif os.name=="nt":
            import msvcrt
            stream.seek(0,os.SEEK_END)
            if stream.tell()==0:
                stream.write(b"0"); stream.flush()
            stream.seek(0)
            try: msvcrt.locking(stream.fileno(),msvcrt.LK_NBLCK,1)
            except OSError as exc:
                raise RuntimeError("another runner holds "+str(path)) from exc
            try: yield
            finally:
                stream.seek(0); msvcrt.locking(stream.fileno(),msvcrt.LK_UNLCK,1)
        else:
            raise RuntimeError("unsupported OS locking; use a supported isolated run")

class CaseInterrupted(BaseException):
    def __init__(self,signum,stack):
        self.signum=signum
        self.stack=stack
        super().__init__("interrupted by signal "+str(signum))

@contextmanager
def interruption_handlers():
    old={}
    def handler(signum,frame):
        raise CaseInterrupted(signum,"".join(traceback.format_stack(frame)))
    try:
        for sig in (signal.SIGINT,signal.SIGTERM):
            old[sig]=signal.getsignal(sig)
            signal.signal(sig,handler)
        yield
    finally:
        for sig,handler in old.items(): signal.signal(sig,handler)

def source_identity(root,precision):
    root=Path(root)
    inventory={}
    for path in sorted(root.rglob("*")):
        rel=path.relative_to(root)
        if not path.is_file() or any(x in ("outputs","artifacts","__pycache__") for x in rel.parts):
            continue
        if path.suffix==".py" or path.name in ("boxes.json","requirements.txt","PLAN_BEFORE_DIG_RUN.md","PLAN_R3_BEFORE_RUN.md"):
            inventory[rel.as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    import flint
    return {"source_sha256":digest(inventory),"source_files":inventory,
            "python":platform.python_version(),"python_flint":flint.__version__,
            "precision":precision,
            "environment":{k:os.environ.get(k) for k in
                           ("PYTHONHASHSEED","OMP_NUM_THREADS","OPENBLAS_NUM_THREADS")}}

def _validate_record(record,case_id,name,plan_sha):
    if (record.get("case_id")!=case_id or record.get("name")!=name or
        record.get("plan_sha256")!=plan_sha or record.get("status")!=STATUS):
        raise ValueError("case record does not match the sealed execution plan")
    return record

def histories(work,tests,plan_sha,recover=False):
    all_rows=[]
    for case_id,(name,_) in enumerate(tests):
        folder=work/("%03d"%case_id)
        attempts=[]
        for path in sorted(folder.glob("*.started.json")):
            started=_validate_record(read_json(path),case_id,name,plan_sha)
            result_path=path.with_name(path.name.replace(".started.json",".result.json"))
            if result_path.exists():
                row=_validate_record(read_json(result_path),case_id,name,plan_sha)
                if row.get("result") not in ("PASS","FAIL","INTERRUPTED"):
                    raise ValueError("invalid completed case state")
            elif recover:
                row=dict(started,result="INTERRUPTED",finished_at=utc_now(),elapsed_ns=None,
                         reason="Previous process ended without a durable case result.",
                         traceback=None,
                         traceback_note="No Python traceback is recoverable after an unhandled kill; see stderr log if present.")
                atomic_json(result_path,row,create=True)
            else:
                row=dict(started,result="RUNNING")
            attempts.append(row)
        if folder.exists():
            for path in folder.glob("*.result.json"):
                if not path.with_name(path.name.replace(".result.json",".started.json")).exists():
                    raise ValueError("orphan case result: "+str(path))
        all_rows.append({"id":case_id,"name":name,
                         "result":attempts[-1]["result"] if attempts else "PENDING",
                         "attempts":attempts})
    return all_rows

def snapshot(out,work,tests,plan,plan_sha,recover=False):
    rows=histories(work,tests,plan_sha,recover)
    complete=all(x["result"] in ("PASS","FAIL") for x in rows)
    count={name:sum(x["result"]==name for x in rows)
           for name in ("PASS","FAIL","PENDING","RUNNING","INTERRUPTED")}
    report={"status":STATUS,"schema":SCHEMA,"mode":plan["mode"],
            "plan_sha256":plan_sha,"plan_file":str(work/"plan.json"),
            "updated_at":utc_now(),"complete":complete,
            "execution":"COMPLETE" if complete else "INCOMPLETE",
            "all_tests_passed":complete and count["FAIL"]==0,
            "counts":count,"tests":rows}
    atomic_json(out,report)
    return report

def run_suite(tests,mode,out,identity,*,resume=False,max_cases=None,
              selected=None,retry_failed=False,precision_context=nullcontext):
    tests=list(tests); out=Path(out)
    if max_cases is not None and (type(max_cases) is not int or max_cases<1):
        raise ValueError("max_cases must be a positive integer")
    if selected is not None and any(i<0 or i>=len(tests) for i in selected):
        raise ValueError("case id outside fixed suite")
    work=out.with_name(out.name+".cases")
    work.mkdir(parents=True,exist_ok=True)
    plan={"status":STATUS,"schema":SCHEMA,"mode":mode,"identity":identity,
          "cases":[{"id":i,"name":name} for i,(name,_) in enumerate(tests)]}
    plan_sha=digest(plan)
    with exclusive_lock(work/"runner.lock"):
        pp=work/"plan.json"
        if pp.exists():
            if not resume:
                raise FileExistsError("existing run: use --resume or a new --out")
            if read_json(pp)!=plan:
                raise ValueError("resume rejected: source/environment/suite identity changed; use a NEW --out")
        else:
            if out.exists():
                raise FileExistsError("existing output without an R2 plan; use a NEW --out")
            if any(work.glob("[0-9]*/*.started.json")):
                raise ValueError("case records without a plan")
            atomic_json(pp,plan,create=True)
        report=snapshot(out,work,tests,plan,plan_sha,recover=True)
        executed=0
        for case_id,(name,fn) in enumerate(tests):
            if selected is not None and case_id not in selected: continue
            previous=report["tests"][case_id]
            if previous["result"]=="PASS": continue
            if previous["result"]=="FAIL" and not retry_failed: continue
            if max_cases is not None and executed>=max_cases: break
            folder=work/("%03d"%case_id); folder.mkdir(exist_ok=True)
            attempt=len(previous["attempts"])+1
            stem="%04d"%attempt
            stdout_path=folder/(stem+".stdout.log")
            stderr_path=folder/(stem+".stderr.log")
            started={"status":STATUS,"case_id":case_id,"name":name,"attempt":attempt,
                     "plan_sha256":plan_sha,"started_at":utc_now(),
                     "stdout":str(stdout_path),"stderr":str(stderr_path)}
            atomic_json(folder/(stem+".started.json"),started,create=True)
            report=snapshot(out,work,tests,plan,plan_sha)
            print("START",case_id,name,"attempt",attempt,flush=True)
            began=perf_counter_ns(); interrupted=None
            with stdout_path.open("x",encoding="utf-8",buffering=1) as sout, \
                 stderr_path.open("x",encoding="utf-8",buffering=1) as serr:
                owned_fault_handler=not faulthandler.is_enabled()
                if owned_fault_handler: faulthandler.enable(file=serr,all_threads=True)
                try:
                    with redirect_stdout(sout),redirect_stderr(serr), \
                         interruption_handlers(),precision_context():
                        try:
                            detail=fn()
                            # Detect non-serializable details before committing PASS.
                            canonical(detail)
                            row=dict(started,result="PASS",detail=detail)
                        except CaseInterrupted as exc:
                            interrupted=128+exc.signum
                            row=dict(started,result="INTERRUPTED",signal=exc.signum,
                                     traceback=traceback.format_exc(),interrupted_stack=exc.stack)
                        except KeyboardInterrupt:
                            interrupted=130
                            row=dict(started,result="INTERRUPTED",traceback=traceback.format_exc())
                        except BaseException as exc:
                            row=dict(started,result="FAIL",traceback=traceback.format_exc())
                            # Width failures must retain the observation, not
                            # just a boolean or an assertion traceback.
                            detail=getattr(exc,"diagnostic",None)
                            if detail is not None:
                                canonical(detail)
                                row["detail"]=detail
                        if row.get("traceback"):
                            serr.write(row["traceback"])
                            if row.get("interrupted_stack"): serr.write(row["interrupted_stack"])
                finally:
                    if owned_fault_handler: faulthandler.disable()
                    sout.flush(); os.fsync(sout.fileno())
                    serr.flush(); os.fsync(serr.fileno())
            row["elapsed_ns"]=perf_counter_ns()-began; row["finished_at"]=utc_now()
            atomic_json(folder/(stem+".result.json"),row,create=True)
            report=snapshot(out,work,tests,plan,plan_sha)
            executed+=1
            print(row["result"],case_id,name,flush=True)
            if interrupted is not None: return interrupted
        report=snapshot(out,work,tests,plan,plan_sha)
        print(STATUS,report["execution"],canonical(report["counts"]),flush=True)
        if not report["complete"]: return 2
        return 0 if report["all_tests_passed"] else 1

def cli(case_builder,precision,root):
    ap=argparse.ArgumentParser()
    ap.add_argument("--full",action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--resume",action="store_true")
    ap.add_argument("--max-cases",type=int)
    ap.add_argument("--case",type=int,action="append",dest="selected")
    ap.add_argument("--retry-failed",action="store_true")
    ap.add_argument("--list-cases",action="store_true")
    args=ap.parse_args()
    tests=case_builder(args.full)
    if args.list_cases:
        for i,(name,_) in enumerate(tests): print(i,name)
        return
    mode="full" if args.full else "quick"
    out=args.out or str(Path(root)/"outputs"/("dig_tests_r2_"+mode+".json"))
    from flint import ctx
    code=run_suite(tests,mode,out,source_identity(root,precision),
                   resume=args.resume,max_cases=args.max_cases,
                   selected=set(args.selected) if args.selected is not None else None,
                   retry_failed=args.retry_failed,
                   precision_context=lambda:ctx.workprec(precision))
    raise SystemExit(code)
