"""Exact geometric inclusion for R63_T63 in G7, no floating computation."""
from fractions import Fraction as F
from pathlib import Path
import json
R0=F(63,64); t0=F(63,64)
zlo=R0*2*t0/(1+t0*t0)
rhohi=(1-t0*t0)/(1+t0*t0)
chi_max=1-zlo*zlo
ratio=25*chi_max
assert zlo==F(7938,8065)
assert rhohi==F(127,8065)
assert chi_max==F(2032381,65044225)
assert ratio<1
# ρ²+z²=R², from (1−τ²)²+(2τ)²=(1+τ²)², valid all boxes.
# u²=ρ²/χ ≤1 by χ=ρ²+(1−R²), with χ=0 iff R=τ=1, where value by continuous limit.
o={"status":"DIAGNOSTIC_ONLY / NOT_EVIDENCE","R":["63/64","1"],"tau":["63/64","1"],"lambda":["79/16","5"],"rho_equator_chart":"R*(1-tau*tau)/(1+tau*tau)","z_equator_chart":"R*2*tau/(1+tau*tau)","physical_z":"lambda*z","z_lower_exact":str(zlo),"rho_upper_exact":str(rhohi),"rho2_plus_z2_identity":"R**2 <= 1","chi_upper_exact":str(chi_max),"max_lambda_squared_chi_exact":str(ratio),"z_positive":zlo>0,"chi_le_lambda_inverse_squared":ratio<=1,"u_le_one":"rho**2 <= chi = rho**2 + 1 - R**2","w_le_one":"w**2=lambda**2*chi<=max_lambda**2*chi_max<1","boundary_trace":"At |q|=1, E_z refers to inner trace; boundary condition B remains separate","all_geometry_checks":True}
p=Path(__file__).resolve().parent/"GEOMETRY_FRACTIONS.json"
p.write_text(json.dumps(o,indent=2,sort_keys=True)+"\n")
print(json.dumps(o,sort_keys=True))
