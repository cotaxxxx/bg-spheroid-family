import numpy as np, json, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
H = np.load('centre_hessian_grid.npy'); G = np.load('grid.npy'); c = json.load(open('centre_zero_curves.json'))
fig, ax = plt.subplots(figsize=(6.4, 5.6), dpi=150)
cols = {'h1': '#c0392b', 'h2': '#2471a3', 'h3': '#1e8449'}
lab = {'h1': 'h1 = 0 (shortest axis a1)', 'h2': 'h2 = 0 (middle axis a2)', 'h3': 'h3 = 0 (longest axis a3)'}
for k, pts in c.items():
    if pts: p = np.array(sorted(pts)); ax.plot(p[:, 0], p[:, 1], 'o-', ms=2.5, lw=1.4, color=cols[k], label=lab[k])
ax.plot([1, 1], [1, 12], color='0.3', lw=3, alpha=.35); ax.plot([1, 12], [1, 1], color='0.3', lw=3, alpha=.35)
ax.annotate('prolate edge (s = 1, lambda = t)\nlambda_c^pro = 4.724', (1, 4.724), xytext=(1.6, 9), arrowprops=dict(arrowstyle='->', color='0.3'), fontsize=8)
ax.annotate('oblate edge (t = 1, lambda = 1/s)\n1/lambda_c^ob = 2.451', (2.451, 1), xytext=(4, 1.8), arrowprops=dict(arrowstyle='->', color='0.3'), fontsize=8)
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlim(1, 12); ax.set_ylim(1, 12)
ax.set_xlabel('s = a2 / a1'); ax.set_ylabel('t = a3 / a2'); ax.set_title('Triaxial family: zero curves of the centre Hessian\n(chat scout, non-interval, DIAGNOSTIC_ONLY)', fontsize=10)
ax.legend(fontsize=8, loc='upper right'); fig.tight_layout(); fig.savefig('centre_zero_curves.png')
