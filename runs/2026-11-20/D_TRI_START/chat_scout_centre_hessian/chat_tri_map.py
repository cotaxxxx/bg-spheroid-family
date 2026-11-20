import numpy as np, json, sys
sys.path.insert(0, '.')
from chat_tri_centre import hess_centre
from scipy.optimize import brentq
ls = np.linspace(0, np.log(12), 61); G = np.exp(ls)
H = np.array([[hess_centre(s, t) for t in G] for s in G])   # H[s_idx, t_idx, i]
np.save('centre_hessian_grid.npy', H); np.save('grid.npy', G)
for i in range(3):
    neg = (H[:, :, i] < 0)
    print(f"h{i+1}: negative fraction {neg.mean():.3f}")
# zero curves: for each s, find t where h_i changes sign (and vice versa)
curves = {}
for i in range(3):
    pts = []
    for s in G:
        f = lambda t: hess_centre(s, t)[i]
        vals = [f(t) for t in G]
        for a, b, va, vb in zip(G, G[1:], vals, vals[1:]):
            if va*vb < 0: pts.append((float(s), float(brentq(f, a, b, xtol=1e-6))))
    curves[f"h{i+1}"] = pts
    print(f"h{i+1} zero curve, sample:", [(round(a, 3), round(b, 3)) for a, b in pts[::6]])
json.dump(curves, open('centre_zero_curves.json', 'w'))
