"""Independent check of Codex's C1, C2 table with a fine chord quadrature (384 x 768); non-interval."""
import numpy as np, chat_tri_h3check as H
from scipy.optimize import brentq
f = lambda s, t, i: H.hc(s, t, 384, 768)[i]
codex = {1.02: (4.587373, 4.769024), 1.25: (3.347876, 5.185693), 1.55: (2.340160, 5.528491), 2.05: (1.414329, 5.808891),
         2.45: (1.001002, 5.896200), 3.2: (None, 5.917775), 8: (None, 5.45012)}
for s, (c1, c2) in codex.items():
    r1 = brentq(lambda t: f(s, t, 0), 1.0, 4.8, xtol=1e-7) if c1 else None
    r2 = brentq(lambda t: f(s, t, 1), 4.6, 6.5, xtol=1e-7)
    print(s, 'C1', None if r1 is None else round(r1, 6), 'codex', c1, '| C2', round(r2, 6), 'codex', c2, flush=True)
