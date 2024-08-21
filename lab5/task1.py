import math
import numpy as np 
import sympy

def main():
    vars = ['x', 'y', 'z']
    equations = ['x ** 2 + y ** 2 + z ** 2 - 1', '2 * x ** 2 + y ** 2 - 4 * z', '3 * x ** 2 - 4 * y + z ** 2']
    print(newton(vars, equations))

def newton(vrs, eqs):
    f = sympy.Matrix(eqs)
    f = sympy.lambdify(sympy.symbols(vrs), f)
    W = sympy.Matrix(eqs).jacobian(vrs)
    W = sympy.lambdify(sympy.symbols(vrs), W)
    xp = [1.0] * len(vrs)
    kmax = 100
    k = 0
    while True:
        xc = np.linalg.solve(W(*xp), f(*xp)).reshape([len(vrs),]).tolist()
        k += 1
        if k >= kmax:
            break
        for i in range(len(xp)):
            xp[i] -= xc[i]
        if np.linalg.norm(xc) > 1e-7:
            pass
        else:
            break
    return xp

if __name__ == "__main__":
    main()