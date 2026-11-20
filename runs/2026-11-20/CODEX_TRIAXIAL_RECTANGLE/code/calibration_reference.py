"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Read-only comparison with original C kernel."""
from pathlib import Path
import tempfile,zipfile,subprocess,hashlib,importlib.util,csv,json
import numpy as np
from calibration import ROOT

SOURCE_HASH={'kernel.c':'15920d6b91fca2cac4b9e2e2e4cc76f6d9a116481af5291f417102e4cab54080',
             'common.py':'184214615c8c64db418d810aed75b9909e4e7d987e1270c7e6073e9c971137f1'}

def read_rows(name):
    rows=list(csv.DictReader((ROOT/'out'/name).open()));group={}
    for r in rows:group[(r['shape'],r['mode'],r.get('experiment',''),r.get('half',''))]=r
    return list(group.values())

def main():
    selections=[]
    for name,filename in [('C1A','calibration_c1a_all.csv'),('C2','calibration_extended.csv'),('C4','calibration_normalized.csv')]:
        for r in read_rows(filename):
            pick=(name=='C1A' and int(r['shape']) in [0,31]) or (name=='C2' and r['experiment']=='boundary_box' and int(r['shape']) in [0,31]) or (name=='C4' and r['mode']=='G3_123')
            if pick:selections.append((name,r))
    archive=ROOT/'inputs/TRIAXIAL_FIRST_ATLAS_20261120.zip';records=[]
    with tempfile.TemporaryDirectory(prefix='calibration_reference_') as temp:
        folder=Path(temp)
        with zipfile.ZipFile(archive) as z:
            for base,digest in SOURCE_HASH.items():
                candidates=[n for n in z.namelist() if n.endswith('/code/'+base)]
                assert len(candidates)==1,(base,candidates)
                data=z.read(candidates[0]);assert hashlib.sha256(data).hexdigest()==digest
                (folder/base).write_bytes(data)
        compile_args=['cc','-O2','-shared','-fPIC',str(folder/'kernel.c'),'-lm','-o',str(folder/'kernel.so')]
        subprocess.run(compile_args,check=True,capture_output=True)
        spec=importlib.util.spec_from_file_location('calibration_original_common',folder/'common.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        for name,row in selections:
            s=(int(row['slo'])+int(row['shi']))/(2*65536);t=(int(row['tlo'])+int(row['thi']))/(2*65536)
            q=np.array([(int(row[f'q{i}lo'])+int(row[f'q{i}hi']))/(2*65536) for i in [1,2,3]])
            if row.get('experiment')=='boundary_box':
                q={'G3_123':[2/3,1/3,2/3],'G3_13':[3/5,0,4/5],
                   'G3_23':[0,3/5,4/5],'D12':[3/5,4/5,0]}[row['mode']]
                q=np.array(q)
            values=[]
            for n in [160,320,640]:
                _,g,_=module.ev(s,t,q,n,False)
                value=(g[1]/q[1]-g[0]/q[0])/(s*s-1) if row['mode']=='D12' else g[2]/q[2]
                assert float(row['lower'])<=value<=float(row['upper']),(name,row['shape'],row['mode'],value)
                values.append(float(value))
            records.append({'plan':name,'shape':int(row['shape']),'mode':row['mode'],
                'point':q.tolist(),'s':s,'t':t,'orders':[160,320,640],'values':values,
                'difference_320_640':abs(values[2]-values[1]),'inside_recorded_interval':True})
    summary={'label':'DIAGNOSTIC_ONLY / NOT_EVIDENCE','integrity_status':'consistent',
       'source_hashes':SOURCE_HASH,'compiler_flags':['-O2','-shared','-fPIC','-lm'],
       'source_policy':'Exact original kernel.c and common.py read from supplied zip; compiled in a temporary directory; originals were not changed.',
       'role':'Non-interval original-C quadrature comparison. Its refinement differences are not rigorous quadrature error bounds and do not change any interval result.',
       'records':records,'max_difference_320_640':max(x['difference_320_640'] for x in records)}
    (ROOT/'out/calibration_reference.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'label':summary['label'],'cases':len(records),'inside_recorded_interval':True,
          'max_difference_320_640':summary['max_difference_320_640']},indent=2))

if __name__=='__main__':main()
