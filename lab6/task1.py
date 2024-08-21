import math
import numpy as np 

def main():
    x, y, table = readTable("data1.txt")
    tmp = [gaussQuadrature(x[:11-i], table[i][:11-i].copy()) for i in range(11)]
    print("Значение без выравнивания: {:f}".format(simpson(y[:11], tmp)))
    tmp = [gaussQuadrature(x[:11-i], table[i][:11-i].copy(), True) for i in range(11)]
    print("Значение с выравниванием: {:f}".format(simpson(y[:11], tmp)))

def readTable(filename):
    fin = open(filename, "r")
    x = list(map(float, fin.readline().split()))
    y = []
    table = []
    for i in range(len(x)):
        tmp = list(map(float, fin.readline().split()))
        y.append(tmp[0])
        table.append(tmp[1:])
    fin.close()
    return x, y, table

lcoefs = [
    [1],
    [1,      0],
    [3,      0, -1],
    [5,      0, -3,       0],
    [35,     0, -30,      0, 3],
    [63,     0, -70,      0, 15,      0],
    [231,    0, -315,     0, 105,     0, -5],
    [429,    0, -693,     0, 315,     0, -35,      0],
    [6435,   0, -12012,   0, 6930,    0, -1260,    0, 35],
    [12155,  0, -25740,   0, 18018,   0, -4620,    0, 315,    0],
    [46189,  0, -109395,  0, 90090,   0, -30030,   0, 3465,   0, -63],
    [88179,  0, -230945,  0, 218790,  0, -90090,   0, 15015,  0, -693,   0],
    [676039, 0, -1939938, 0, 2078505, 0, -1021020, 0, 225225, 0, -18018, 0, 231]
]

def gaussQuadrature(x, y, needAlign = False):
    n = len(x)
    y0 = y.copy()
    if needAlign:
        for i in range(n):
            if y0[i] > 1e-7:
                y0[i] = math.log(y0[i])
            else:
                y0[i] = float("-inf")
    koefs = sorted(np.roots(lcoefs[n]).tolist())
    tmp = [1.0 for i in range(n)]
    matr = []
    ans = []
    for i in range(n):
        matr.append(tmp.copy())
        if i % 2 == 0:
            ans.append(2 / (i + 1))
        else:
            ans.append(0)
        for j in range(n):
            tmp[j] *= koefs[j]
    if n > 1:
        A = np.linalg.solve(matr, ans).tolist()
    else:
        A = [2]
    for i in range(n):
        koefs[i] = koefs[i] * (x[-1] - x[0]) / 2 + (x[-1] + x[0]) / 2
    integral = 0
    for i in range(n):
        integral += A[i] * newtonInterpolation(x, y0, koefs[i], needAlign)
    integral *= (x[-1] - x[0]) / 2
    return integral

def newtonInterpolation(x, y, x0, needAlign = False):
    table = [y]
    i = 0
    while len(table[-1]) > 1:
        table.append([0] * (len(table[i]) - 1))
        for j in range(len(table[i]) - 1):
            table[i + 1][j] = (table[i][j] - table[i][j + 1]) / (x[j] - x[j + i + 1])
        i += 1
    res = table[0][0]
    xp = x0 - x[0]
    for i in range(1, len(table)):
        res += table[i][0] * xp
        xp *= x0 - x[i]
    if needAlign:
        res = math.exp(res)
    return res

def simpson(x, y):
    integral = 0.0
    for i in range(len(x) // 2):
        integral += ((x[2 * i + 2] - x[2 * i]) / 6) * (y[2 * i] + 4 * y[2 * i + 1] + y[2 * i + 2])
    return integral

if __name__ == "__main__":
    main()