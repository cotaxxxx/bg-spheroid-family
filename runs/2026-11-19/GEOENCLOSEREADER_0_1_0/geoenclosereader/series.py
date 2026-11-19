"""Positive h-series for F = pi^2/4 - alpha^2, alpha = arccos(gamma), h = (1 - gamma)/2.

F' = P = 2 alpha / sin alpha = 2 sum a_n h^n,   a_n = 4^n (n!)^2 / (2n+1)!
Q = 2F' + gamma F'' = sum q_n h^n,            q_n = a_n (2n^2 + 10n + 10)/(2n + 3)
Tails (all terms >= 0, h in [0, 1/2]): P tail <= 4 a_M h^M,  Q tail <= (2N + 12) a_M h^M,  M = N + 1.
"""
from math import factorial
from flint import arb, fmpq

NS = 24
A = [fmpq(4**n*factorial(n)**2, factorial(2*n+1)) for n in range(NS+2)]
QC = [A[n]*fmpq(2*n*n+10*n+10, 2*n+3) for n in range(NS+1)]


def P_enc(g):
    h = (1-g)/2
    s = 2*sum((arb(A[n])*h**n for n in range(NS+1)), arb(0))
    return s + arb(0).union(4*arb(A[NS+1])*h**(NS+1))


def Q_enc(g):
    h = (1-g)/2
    s = sum((arb(QC[n])*h**n for n in range(NS+1)), arb(0))
    return s + arb(0).union(arb(2*NS+12)*arb(A[NS+1])*h**(NS+1))
