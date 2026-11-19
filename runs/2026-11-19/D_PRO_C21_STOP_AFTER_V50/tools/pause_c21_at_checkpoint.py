#!/usr/bin/env python3
"""Judge-directed suspension at a committed C21 checkpoint. Never terminates.

SIGSTOP/SIGCONT are addressed through pidfds to these exact two processes only.
No solver source, STATE, SUMMARY, registry, or existing ledger is written.
The result is a suspended process, not a normal-exit or completed-session claim.
"""
import collections
import ctypes
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import select
import signal
import time
from fractions import Fraction as F

ROOT = Path('/home/daybreak/D_PRO_C21_H_HEAVY_SLAB_20261118/worktree')
RUN = ROOT / 'runs/2026-11-18/D_PRO_C21_H_HEAVY_SLAB'
OUT = ROOT.parent / 'stop_20261119'
LOG = RUN / 'RESUME_CONTINUOUS.log'
EXPECTED = {1581407: 250927160, 1581409: 250927161}
CONTROLLER = 1581409
PARENT = 1581407
COVER_SHA = 'bf111ee4672927d858afe3572e4d61c1c728818e3673b4ee89e441d9f211819e'
SOURCE = ROOT / 'prolate_r4/c21_heavy_cover.py'
LOCK = Path('/tmp/d_pro_c21_heavy_slab_20261118.lock')

def need(value, reason):
    if not value:
        raise RuntimeError(reason)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def stamp():
    now = dt.datetime.now(dt.timezone.utc)
    return {'utc': now.isoformat(), 'jst': now.astimezone(dt.timezone(dt.timedelta(hours=9))).isoformat()}

def save(name, obj):
    path = OUT / name
    raw = (json.dumps(obj, indent=2, sort_keys=True) + '\n').encode()
    temp = path.with_suffix(path.suffix+'.tmp')
    with temp.open('wb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    os.replace(temp, path)
    fd = os.open(OUT, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)

def proc(pid):
    try:
        parts = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()
    except FileNotFoundError:
        return None
    need(int(parts[19]) == EXPECTED[pid], 'PID_IDENTITY_CHANGED')
    return {'pid': pid, 'state': parts[0], 'start_ticks': int(parts[19]),
            'user_ticks': int(parts[11]), 'system_ticks': int(parts[12])}

def children():
    ids = set()
    for task in Path(f'/proc/{CONTROLLER}/task').iterdir():
        try:
            ids.update(map(int, (task/'children').read_text().split()))
        except FileNotFoundError:
            pass
    return sorted(ids)

def threads_stopped():
    tasks = list(Path(f'/proc/{CONTROLLER}/task').iterdir())
    return bool(tasks) and all(p.joinpath('stat').read_text().rsplit(')',1)[1].split()[0] == 'T' for p in tasks)

def checkpoint():
    raw = (RUN/'STATE.json').read_bytes()
    summary_raw = (RUN/'SUMMARY.json').read_bytes()
    st, summary = json.loads(raw), json.loads(summary_raw)
    need(st['plate'] == ['79/16','5'] and st['workers'] == 12 and st['global_36h_cap_s'] == 129600, 'PLAN_CHANGED')
    need(not st['inflight'], 'INFLIGHT_NOT_EMPTY')
    active = [t['node'] for t in st['terminal']] + st['pending']
    def area(n):
        a,b,c,d = [F(x) for k in ('R','tau') for x in n[k]]
        need(0 <= a < b <= 1 and 0 <= c < d <= 1, 'INVALID_RECTANGLE')
        return (b-a)*(d-c)
    ids = [n['id'] for n in active]
    need(len(ids) == len(set(ids)), 'DUPLICATE_ACTIVE_NODE')
    byroot = collections.defaultdict(F)
    for n in active:
        byroot[n['root']] += area(n)
    need(len(byroot) == 4096 and all(v == F(1,4096) for v in byroot.values()), 'ROOT_AREA_MISMATCH')
    decided = [t for t in st['terminal'] if t['kind'] == 'DECIDED_NONZERO']
    tube = [t for t in st['terminal'] if t['kind'] != 'DECIDED_NONZERO']
    counts = {'attempted_terminal_or_split_nodes':len(st['processed']),
              'decided_count':len(decided), 'tube_evaluated_count':len(tube),
              'pending_unprocessed_count':len(st['pending']),
              'decided_area_exact':str(sum((area(t['node']) for t in decided),F(0))),
              'tube_area_exact':str(sum((area(t['node']) for t in tube),F(0))),
              'pending_area_exact':str(sum((area(n) for n in st['pending']),F(0))),
              'area_total_exact':'1'}
    need(all(summary[k] == v for k,v in counts.items()), 'SUMMARY_CHECKPOINT_MISMATCH')
    return st, {'STATE.json':sha(raw), 'SUMMARY.json':sha(summary_raw)}, counts

def last_batch():
    # Unbuffered print can emit several writes; only a newline-complete record
    # is evidence of a completed checkpoint announcement.
    lines = LOG.read_text().splitlines(keepends=True)
    found = [x.rstrip('\r\n') for x in lines if x.startswith('BATCH ') and x.endswith('\n')]
    need(found, 'NO_BATCH_LOG')
    line = found[-1]
    m = re.fullmatch(r'BATCH (\d+) processed (\d+) decided (\d+) tube (\d+) pending (\d+) wall_s ([0-9.]+)',line)
    need(m is not None, 'UNRECOGNIZED_BATCH_LOG')
    return int(m[1]), float(m[6]), line

def held_lock():
    stat = LOCK.stat()
    matches=[]
    for line in Path('/proc/locks').read_text().splitlines():
        p=line.split()
        if len(p)>=8 and p[1:4]==['FLOCK','ADVISORY','WRITE'] and p[4]==str(PARENT):
            major,minor,inode=p[5].split(':')
            if (int(major,16),int(minor,16),int(inode)) == (os.major(stat.st_dev),os.minor(stat.st_dev),stat.st_ino):
                matches.append(line)
    need(len(matches)==1, 'ORIGINAL_FLOCK_HOLDER_NOT_CONFIRMED')
    return {'device':stat.st_dev,'inode':stat.st_ino,'proc_locks_record':matches[0]}

def main():
    need(sha(SOURCE.read_bytes()) == COVER_SHA, 'FROZEN_CONTROLLER_CHANGED')
    need(not (OUT/'pause_result.json').exists(), 'PREVIOUS_PAUSE_RESULT_EXISTS')
    OUT.mkdir(exist_ok=True)
    original={pid:proc(pid) for pid in EXPECTED}
    need(all(v and v['state'] not in ('T','Z') for v in original.values()), 'ORIGINAL_NOT_RUNNING')
    descriptors={pid:os.pidfd_open(pid) for pid in EXPECTED}
    need(hasattr(signal,'pidfd_send_signal'), 'PIDFD_SIGNAL_UNAVAILABLE')
    libc=ctypes.CDLL(None,use_errno=True)
    fd=libc.inotify_init1(os.O_NONBLOCK | os.O_CLOEXEC)
    need(fd>=0,'INOTIFY_INIT_FAILED')
    watch=libc.inotify_add_watch(fd,os.fsencode(LOG),0x00000002)
    need(watch>=0,'INOTIFY_WATCH_FAILED')
    initial=json.loads((RUN/'STATE.json').read_text())
    initial_batch=initial['completed_batches']
    target=initial_batch+1
    lock=held_lock()
    prepared={'status':'WAITING_FOR_COMMITTED_BATCH','time':stamp(),'target_batch_at_least':target,
              'original_processes':original,'script_sha256':sha(Path(__file__).read_bytes()),
              'source_sha256':COVER_SHA,'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
              'lock':lock,'method':'SIGSTOP suspension only; no termination signals',
              'original_state_modified_by_this_script':False}
    save('pause_prepared.json',prepared)
    print(json.dumps(prepared),flush=True)
    attempts=[]
    controller_paused=False
    valid_checkpoint=False
    try:
        while True:
            need(all(proc(pid) is not None for pid in EXPECTED),'ORIGINAL_ALREADY_EXITED')
            ready=select.select([fd],[],[],1)[0]
            if not ready:
                continue
            os.read(fd,65536)
            batch,elapsed,line=last_batch()
            if batch<target:
                continue
            # An event delayed beyond the immediate new-batch window is ignored.
            if time.time()-LOG.stat().st_mtime>0.5 or children():
                target=batch+1
                continue
            global_left=129600-initial['wall_elapsed_cumulative_s']-elapsed
            need(global_left>60,'TOO_CLOSE_TO_ORIGINAL_CAP_FOR_SUSPENSION')
            proc(CONTROLLER)
            t=time.monotonic()
            signal.pidfd_send_signal(descriptors[CONTROLLER],signal.SIGSTOP)
            controller_paused=True
            while not threads_stopped() and time.monotonic()-t<0.2:
                time.sleep(0.001)
            if not threads_stopped() or children():
                signal.pidfd_send_signal(descriptors[CONTROLLER],signal.SIGCONT)
                controller_paused=False
                attempts.append({'batch':batch,'result':'RESUMED_IMMEDIATELY_NOT_QUIESCENT','seconds':time.monotonic()-t})
                target=batch+1
                continue
            try:
                st,hashes,counts=checkpoint()
                b,checkpoint_elapsed,last_line=last_batch()
                need(st['completed_batches']==b and b>=target,'BATCH_CHECKPOINT_MISMATCH')
            except Exception as exc:
                signal.pidfd_send_signal(descriptors[CONTROLLER],signal.SIGCONT)
                controller_paused=False
                attempts.append({'batch':batch,'result':'RESUMED_CHECKPOINT_NOT_READY','reason':str(exc),'seconds':time.monotonic()-t})
                target=batch+1
                continue
            valid_checkpoint=True
            # No children exist here; all computation is already quiescent.
            current_lock=held_lock()
            need((current_lock['device'],current_lock['inode']) ==
                 (lock['device'],lock['inode']),'LOCK_CHANGED')
            proc(PARENT)
            signal.pidfd_send_signal(descriptors[PARENT],signal.SIGSTOP)
            for _ in range(200):
                if proc(PARENT)['state']=='T':break
                time.sleep(0.001)
            need(proc(PARENT)['state']=='T' and threads_stopped() and not children(),'SUSPENSION_NOT_CONFIRMED')
            time.sleep(0.1)
            st2,hashes2,counts2=checkpoint()
            need(hashes2==hashes and counts2==counts,'CHECKPOINT_NOT_STABLE')
            need(sha(SOURCE.read_bytes())==COVER_SHA,'SOURCE_CHANGED')
            result={**prepared,'status':'SUSPENDED_WITH_COMMITTED_CHECKPOINT','time':stamp(),
                    'completed_batches':b,'checkpoint_hashes':hashes,'checkpoint_counts':counts,
                    'inflight':0,'worker_children':[], 'processes':{pid:proc(pid) for pid in EXPECTED},
                    'original_exit_code':None,'normal_session_finalization':False,
                    'original_sessions_count':len(st2['sessions']),
                    'state_cumulative_before_live_session_seconds':st2['wall_elapsed_cumulative_s'],
                    'checkpoint_session_elapsed_seconds_from_log':checkpoint_elapsed,
                    'checkpoint_cumulative_seconds_from_log':st2['wall_elapsed_cumulative_s']+checkpoint_elapsed,
                    'last_batch_log':last_line,'attempts':attempts,
                    'ram_program_counter_not_claimed':'Disk checkpoint committed; RAM may be before next dispatch.',
                    'automatic_continuation':'NOT_INSTALLED; CANCELLED_BY_JUDGE_STOP_INSTRUCTION'}
            save('pause_result.json',result)
            print(json.dumps(result),flush=True)
            return
    except BaseException as exc:
        # A failed unverified candidate must not leave live workers without
        # their controller timeout supervision. Preserve a verified suspension.
        resume_error=None
        if controller_paused and not valid_checkpoint:
            try:
                signal.pidfd_send_signal(descriptors[CONTROLLER],signal.SIGCONT)
                controller_paused=False
            except Exception as resume_exc:
                resume_error=type(resume_exc).__name__+':'+str(resume_exc)
        save('pause_error.json',{'time':stamp(),'error':type(exc).__name__+':'+str(exc),
                               'controller_suspended':controller_paused,'valid_checkpoint':valid_checkpoint,
                               'resume_error':resume_error,'attempts':attempts,
                               'processes':{pid:proc(pid) for pid in EXPECTED}})
        raise

if __name__=='__main__':
    main()
