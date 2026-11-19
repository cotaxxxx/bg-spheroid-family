#!/usr/bin/env python3
"""Archive a verified, suspended C21 run into a separate new branch worktree."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
from fractions import Fraction as F

BASE=Path('/home/daybreak/D_PRO_C21_H_HEAVY_SLAB_20261118')
ORIGINAL=BASE/'worktree'
RUN=ORIGINAL/'runs/2026-11-18/D_PRO_C21_H_HEAVY_SLAB'
OPS=BASE/'stop_20261119'
WORK=BASE/'stop_archive_worktree'
REL=Path('runs/2026-11-19/D_PRO_C21_STOP_AFTER_V50')
DEST=WORK/REL
BRANCH='research/d-pro-c21-stopped-v50-20261119'
BASE_COMMIT='c86c10d4db81614256909ef0cdf1c98fa7240686'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(name,obj):
 p=DEST/name;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(obj,f,indent=2,sort_keys=True);f.write('\n')
def process(pid,ticks):
 s=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
 assert int(s[19])==ticks and s[0]=='T',(pid,s[0])
 return {'pid':pid,'state':s[0],'start_ticks':int(s[19])}
def git(*args,cwd=WORK):
 r=subprocess.run(['git',*args],cwd=cwd,capture_output=True,text=True)
 assert r.returncode==0,(args,r.stderr)
 return r.stdout.strip()

def main():
 assert git('branch','--show-current')==BRANCH
 assert git('rev-parse','HEAD')==BASE_COMMIT
 assert not git('status','--porcelain')
 assert not DEST.exists()
 pause=json.loads((OPS/'pause_result.json').read_text())
 audit=json.loads((OPS/'AREA_SIGN_AUDIT.json').read_text())
 assert pause['status']=='SUSPENDED_WITH_COMMITTED_CHECKPOINT'
 assert audit['audit_status']=='PASS' and not audit['errors']
 assert audit['checkpoint']['inflight_count']==0 and audit['exact_area']['total']=='1'
 assert audit['checkpoint']['completed_batches']==pause['completed_batches']
 processes=[process(1581407,250927160),process(1581409,250927161)]
 for t in Path('/proc/1581409/task').iterdir():
  assert not (t/'children').read_text().strip()
 for name,h in pause['checkpoint_hashes'].items():assert sha(RUN/name)==h
 original_head=git('rev-parse','HEAD',cwd=ORIGINAL)
 assert original_head=='6c206a22aefd07340d4e2df0974b6487bdc836a3'
 assert not git('diff','--name-only','--','prolate_r4',cwd=ORIGINAL)
 files=sorted(p for p in RUN.rglob('*') if p.is_file())
 assert not any(p.is_symlink() for p in files)
 manifest=[{'path':p.relative_to(RUN).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]
 DEST.mkdir(parents=True)
 archive=DEST/'ORIGINAL_RUN_SNAPSHOT.tar.gz'
 with tarfile.open(archive,'w:gz',compresslevel=6) as tf:
  for p in files:tf.add(p,arcname='original_run/'+p.relative_to(RUN).as_posix(),recursive=False)
 # Verify every archived byte against a current-snapshot manifest.
 expected={'original_run/'+m['path']:m for m in manifest}
 checked=0
 with tarfile.open(archive,'r:gz') as tf:
  for member in tf:
   assert member.isfile() and member.name in expected
   data=tf.extractfile(member).read();m=expected[member.name]
   assert len(data)==m['bytes'] and hashlib.sha256(data).hexdigest()==m['sha256']
   checked+=1
 assert checked==len(expected)
 for m in manifest:assert sha(RUN/m['path'])==m['sha256'],'Original input changed'
 (DEST/'SNAPSHOT_SHA256SUMS').write_text(''.join(m['sha256']+'  original_run/'+m['path']+'\n' for m in manifest))
 write('SNAPSHOT_MANIFEST.json',{'snapshot_source':str(RUN),'files':manifest,'file_count':len(manifest),
       'total_source_bytes':sum(m['bytes'] for m in manifest),'archive':archive.name,'archive_sha256':sha(archive),
       'archive_verified_entries':checked,'historical_manifests_preserved':'original_run/SHA256SUMS is the earlier initial-run manifest; SNAPSHOT_SHA256SUMS is authoritative for this snapshot.'})
 copies={'pause_result.json':'STOP_RECEIPT.json','pause_prepared.json':'STOP_PREPARATION.json',
         'pause_driver.log':'STOP_DRIVER.log','AREA_SIGN_AUDIT.json':'AREA_SIGN_AUDIT.json',
         'DIG_INSTRUCTION_STOP_HEAVY_SLAB_20261119.md':'DIG_INSTRUCTION_STOP_HEAVY_SLAB_20261119.md',
         'pause_c21_at_checkpoint.py':'tools/pause_c21_at_checkpoint.py',
         'verify_stopped_snapshot.py':'tools/verify_stopped_snapshot.py',
         'CHAT_ADDITIONAL_WINDOW_AUDIT_20261119.zip':'CHAT_ADDITIONAL_WINDOW_AUDIT_20261119.zip'}
 for src,dest in copies.items():
  p=DEST/dest;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(OPS/src,p)
 shutil.copy2(__file__,DEST/'tools/archive_stopped_run.py')
 sources={str(p.relative_to(ORIGINAL)):sha(p) for p in sorted((ORIGINAL/'prolate_r4').glob('*.py'))}
 write('SOURCE_HASHES.json',{'original_head':original_head,'source_files':sources,'source_git_diff_empty':True})
 write('CONTINUATION_CANCELLED.json',{'status':'CANCELLED_BEFORE_DEPLOYMENT','time_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
       'reason':'Judge DIG_INSTRUCTION_STOP_HEAVY_SLAB_20261119.md supersedes the continuation ruling 1d4271a.',
       'prepared_script_sha256':'5b08585003e23b34e0da019738daebc871f38a2fa3e9537727666c7ed55223f6',
       'deployed_to_research_pc':False,'armed':False,'watch_process_started':False,'continuation_started':False,
       'scheduled_C21_automation_created':False,'local_preparation_tests':{'guard_fixtures':23,'lock_mechanism_fixtures':4,'budget_fixtures':3}})
 write('SNAPSHOT_RECEIPT.json',{'status':'DIAGNOSTIC_ONLY / NOT_EVIDENCE','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
       'branch':BRANCH,'branch_base':BASE_COMMIT,'original_worktree':str(ORIGINAL),'original_head':original_head,
       'snapshot_directory':str(DEST),'original_processes':processes,'original_files_rewritten_by_archive_script':False,
       'main_modified_by_this_work':False,'canonical_STATE_modified_by_this_work':False,
       'stop_instruction_sha256':sha(OPS/'DIG_INSTRUCTION_STOP_HEAVY_SLAB_20261119.md'),
       'archive_sha256':sha(archive),'snapshot_files':len(manifest),'H_positive_count':audit['positive_H_count'],
       'checkpoint_batch':pause['completed_batches'],'archive_contains_uncommitted_tmp':any(m['path'].endswith('.tmp') for m in manifest)})
 cumulative=pause['checkpoint_cumulative_seconds_from_log']
 hours=int(cumulative//3600);minutes=int(cumulative%3600//60);seconds=cumulative%60
 readme=f'''# 旧 C21 重い板の停止・途中記録 — 2026-11-19

**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

Judge の停止指示に従い、旧本走の計算を停止した。対象は **λ=[79/16,5]、幅1/16**。
停止時刻は **2026-11-19 19:27:42 JST**、最終の確定バッチは **245** である。

## 停止の状態

PID 1581407（flock）と1581409（controller）は **SIGSTOPによる一時停止状態 T**。
全controller threadの停止、子worker 0、STATEのinflight 0、STATE/SUMMARYの一致、
元lockの保持を確認した。最初の候補で成功し、STOP→CONTの再試行は0回。
SIGTERM/SIGKILLは送っていない。通常終了ではなく、終了コードと新しいSESSION_SUMMARYはない。
RAM内の命令位置をBATCH直後と断定せず、確定したディスクcheckpointとの整合を記録する。
自動再開は行わない。ソース、元STATE、元SUMMARYを停止処理から書き換えていない。

現行runnerには実行中の通常停止入口がなく、SIGINTも無視される。
このためバッチ確定後・子計算なしの候補に限って停止し、その後に整合を検証した。
詳細は [STOP_RECEIPT.json](STOP_RECEIPT.json) と [停止スクリプト](tools/pause_c21_at_checkpoint.py)。

## 確定した件数と面積

| 区分 | 箱数 | R–τの厳密な面積 |
|---|---:|---:|
| H<0 と判定済み | 1118 | 559/2048 |
| H>0 と判定済み | 0 | 0 |
| Hの零包含による最小幅の管 | 0 | 0 |
| 既知の特別予約OPEN R63_T63 | 1 | 1/4096 |
| その他OPEN | 0 | 0 |
| 未処理pending | 4798 | 2977/4096 |
| 実行中inflight | 0 | 0 |
| 合計 | 5917 | 1 |

元STATEのtube=1は、既知のR63_T63のTUBE_OPEN_ERRORである。
H≈0が観測された管としては数えず、SPECIAL_RESERVED_AXIS_BOUNDARY_CORNERとして
面積を一度だけ計上する。元STATEのラベルは変更していない。

処理記録は2940件（Hを評価した2939件、既知OPEN 1件）。
零を含む区間から二分した親は1821件で、確定した最小管ではない。
未処理は、幅(R,τ)=(1/64,1/64)の1156箱と、(1/128,1/64)の3642箱。

## H>0 の照合

全2940件の元boxes JSONを読み、STATEとの入力λ・R・τ、route、H区間を照合した。
**判定済み1118箱はすべてH<0。H>0の記録は0件。**
分割親を含む全処理済みJSONでも、正のH区間は0件だった。
独立検査はPASS、errors=[]。正の候補リストは空なので、該当する端点の列挙はない。
未処理領域への旧C21の結論は拡張しない。
V50の「この板の全体でH<0」と矛盾する確定箱は見つからなかった。

[AREA_SIGN_AUDIT.json](AREA_SIGN_AUDIT.json) に全件の原物SHA、残箱の座標・幅・分布を記録した。
4,096根の各面積1/4096、分割木の子、重複・欠落、全体の面積総和1もFractionで検証した。
これは記録と被覆構造の検査であり、H/Wの再計算ではない。

## 経過時間

最終BATCHログの85286.93秒に、先行sessionの545.4663487360813秒を加えると、
**{cumulative:.6f}秒（約{hours}時間{minutes}分{seconds:.2f}秒）**。
ログの値は0.01秒単位の丸めを含む。停止後のpsの経過時間は停止中も増えるので使わない。
元STATEの累積値545.466…秒はsession正常終了時に更新される設計であり、手で補正していない。
旧板の完走実績は得ていないため、λ幅1あたりの完了費用の実績値は作っていない。

## 保全と継続の中止

- 原runの全{len(manifest)}ファイルを [ORIGINAL_RUN_SNAPSHOT.tar.gz](ORIGINAL_RUN_SNAPSHOT.tar.gz) に原bytesで保全した。
- [SNAPSHOT_SHA256SUMS](SNAPSHOT_SHA256SUMS) と [SNAPSHOT_MANIFEST.json](SNAPSHOT_MANIFEST.json) は停止時点の全ファイルを対象にする。
- 原runにあった過去のSHA256SUMSも改変せず収録している。これは初回実行時の歴史記録である。
- archiveを読み戻して全{checked}項目を照合し、その後の原ファイルの再hashも一致した。
- 追加36時間の見張りは、コード作成・局所検査までで設置前に中止。自動継続は未実施。
- 新branchへの追加だけであり、main・正本STATE・既存の台帳は編集していない。

原run archive SHA-256:

```text
{sha(archive)}
```

停止時STATE SHA-256:

```text
{pause['checkpoint_hashes']['STATE.json']}
```

## 採用結果との関係・追加点検

Judge指示はV49 `cb38e50` とV50 `854c553448db680634bfc599fd222f97f6c13b7b` の研究採用を明記する。
これを受けて旧本走を止めた。停止指示の原文も同梱した。
[CHAT_ADDITIONAL_WINDOW_AUDIT_20261119.zip](CHAT_ADDITIONAL_WINDOW_AUDIT_20261119.zip) は、この対話で別途行った
窓パッケージのreplay、独立有理数による台帳構造検査、角度表255行・P/Q表2049行の
有理数による包含検査、数式・区間コードの一次点検の記録である。
採用判断をやり直したり、既存V50記録を書き換えたりするものではない。
'''
 (DEST/'README.md').write_text(readme)
 deliverables=sorted(p for p in DEST.rglob('*') if p.is_file())
 (DEST/'DELIVERABLE_SHA256SUMS').write_text(''.join(sha(p)+'  '+p.relative_to(DEST).as_posix()+'\n' for p in deliverables))
 print(json.dumps({'directory':str(DEST),'branch':BRANCH,'source_files':len(manifest),
       'archive_bytes':archive.stat().st_size,'archive_sha256':sha(archive),
       'H_positive_count':audit['positive_H_count'],'audit_status':audit['audit_status']}))

if __name__=='__main__':main()
