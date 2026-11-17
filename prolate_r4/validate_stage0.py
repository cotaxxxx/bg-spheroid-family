"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Check saved Stage0 results against pinned budgets and numerical reference."""
import argparse,json
from fractions import Fraction as Q
from pathlib import Path

def main(root):
    d=Path(root)
    x=json.loads((d/'stage0_split4.json').read_text())
    b=json.loads((d/'majorant_split4.json').read_text())
    reference=json.loads((d/'reference50_replay.json').read_text())
    pre=json.loads((d/'stage1_preflight.json').read_text())
    assert len(x['coefficients'])==len(reference['coefficients'])==35
    ref_ok=[]
    for interval,item in zip(x['coefficients'],reference['coefficients']):
        assert interval['alpha']==item['alpha']
        a,z=map(Q,interval['integral'])
        v=Q(item['value'])
        ref_ok.append(a<=v<=z)
    coeff=Q(x['total_halfwidth_sum'])
    tail=Q(b['partial_tail_for_convergent_cells'])
    amax=Q(b['max_A'])
    # Preset independent contracts: sum of coefficient radii <=1e-5,
    # tail <= 0.03 times the stage0 physical measure 1/1024,
    # maximum positive-denominator relative variation <= 1/8.
    budgets={'coefficient':'1/100000','tail':'3/102400','max_A':'1/8'}
    verdict=(all(ref_ok) and coeff<=Q(budgets['coefficient'])
       and tail<=Q(budgets['tail']) and amax<=Q(budgets['max_A'])
       and x['spatial_cells']==64 and b['cells']==64
       and b['nonconforming_count']==0)
    result={'status':'DIAGNOSTIC_ONLY / NOT_EVIDENCE',
       'scope':'single spatial cell only','stage0_verdict':'PASS' if verdict else 'FAIL',
       'all_35_references_contained':all(ref_ok),'reference_count':len(ref_ok),
       'coefficient_halfwidth_sum':str(coeff),'tail_upper':str(tail),
       'sum_of_coefficient_halfwidths_plus_tail':str(coeff+tail),
       'max_A':str(amax),'prespecified_budgets':budgets,
       'stage0_measure':'1/1024',
       'stage1_preflight_samples':pre['points_tested'],
       'stage1_preflight_violations':pre['violating'],
       'stage1_status':'NO_GO_FIXED_THRESHOLD' if pre['violating'] else 'PRECHECK_ONLY',
       'box2_W_enclosure':None,'stage1_executed':False}
    (d/'FINAL_STAGE0_VERDICT.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Stage0:',result['stage0_verdict'],'Stage1:',result['stage1_status'])
    return 0 if verdict else 1
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--runs',required=True)
    raise SystemExit(main(ap.parse_args().runs))
