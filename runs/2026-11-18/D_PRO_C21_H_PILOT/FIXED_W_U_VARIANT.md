# W B4 auxiliary variant U — independent pre-run freeze
2026-11-18 / DIAGNOSTIC_ONLY / NOT_EVIDENCE

The previously frozen axis-depth-16 spatial h/v/w rule is NOT
reinterpreted: its four children all STOPPED at LEAF_LIMIT=32768.
This is a **second explicit independent diagnostic** based on the
other alternative permitted in Judge's C21 instruction.

Map the spatial h coordinate through u=tan(psi/4) in [0,1], so
 h(u)=1-8u^2/(1+u^2)^2 is monotone from h(0)=1 to h(1)=-1.
Initial u breakpoints are fixed rational:
[0, 1/64, 1/32, 1/16, 1/8, 1/4, 1/2, 1].
Use the v3 azimuth and w breakpoints unchanged:
v [0,1/4,1/2,3/4,1],
w [0,1/16,1/8,1/4,1/2,1].
Each u cell is converted by exact rational endpoints to its
corresponding h interval BEFORE calling the old CW7 majorant.
The correct normalized measure is the EXACT h-width:
 (h(u_lo)-h(u_hi))*delta_v*delta_w/2.
Do not replace that measure by du*dv*dw.
No transformed density or approximate Jacobian is needed.

Keep V35 option-a R x tau 2x2, lambda unsplit, per-child
 max A_j(1)<=1/4 and full spatial B4 integral <=3/100.
Split longest normalized available (u,v,w) side, tie u,v,w.
Per-axis split count cap 16, leaf cap 32768, 60s per child.
Tail-first refinement of largest rigorous measure*B4 contribution
as before. NO W 35-coefficient integration unless all four
full-domain B4 covers succeed. Any incomplete result stays OPEN.
