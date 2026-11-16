"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Rational-endpoint reciprocal regression."""
import json
from flint import fmpq as Q
from ..kernel import V_box_details,STATUS,hull


def main():
    # Positive exact lower endpoint, despite a radius-rounded ball crossing 0.
    tiny=Q(1,10**30)
    assert not hull(tiny,Q(1,64)) > 0
    r=V_box_details((tiny,Q(1,64)),(Q(1,2),Q(33,64)),(Q(2),Q(513,256)),128)
    assert r.route=='Ez_over_z' and r.enclosure.is_finite() and r.lower.is_finite()
    print(json.dumps({'status':STATUS,'result':'PASS','test':'positive rational z interval with ball inflation',
                      'route':r.route,'lower':str(r.lower.fmpq()),'cells':r.cells}))


if __name__=='__main__':
    try:main()
    except Exception:
        print(json.dumps({'status':STATUS,'result':'FAIL','test':'positive rational z interval with ball inflation'}))
        raise
