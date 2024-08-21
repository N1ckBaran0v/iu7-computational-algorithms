import random as rnd 
from scipy.linalg import solve
import numpy as np
import matplotlib.pyplot as plt

class Table:

    def __init__(self):
        self.table = []
        self.sizes = 0

    def setSizes(self, newSizes):
        if newSizes == 1 or newSizes == 2:
            self.sizes = newSizes
        else:
            raise RuntimeError('Неправильная размерность аппроскимации (нужна 1 или 2)')

    def generate(self):
        ptrb = ""
        print("Ввод числа точек по x.")
        x0 = xn = -1
        nx = readNum(1, 10)
        if nx > 0:
            x0 = readFloat(-10, 10)
        if x0 >= -10:
            xn = readFloat(x0, x0 + 20)
        y0 = yn = -1
        ny = 1
        if self.sizes == 2 and xn >= x0:
            print("Ввод числа точек по y.")
            ny = readNum(1, 10)
            if ny > 0:
                y0 = readFloat(-10, 10)
            if y0 >= -10:
                yn = readFloat(y0, y0 + 20)
            if yn < y0:
                xn = x0 - 1
        if xn >= x0:
            tmp = []
            xd = 0
            x = x0
            if nx > 1:
                xd = (xn - x0) / (nx - 1)
            for i in range(nx):
                if self.sizes == 1:
                    tmp.append(TableLine())
                    tmp[-1].x = x
                    tmp[-1].y = func1(x)
                    tmp[-1].r = 1
                else:
                    y = y0
                    yd = 0
                    if ny > 1:
                        yd = (yn - y0) / (ny - 1)
                    for j in range(ny):
                        tmp.append(TableLine())
                        tmp[-1].x = x
                        tmp[-1].y = y
                        tmp[-1].z = func2(x, y)
                        tmp[-1].r = 1
                        y += yd
                x += xd
            self.table = tmp

    def readFromFile(self, filename):
        fin = fopen(filename, "r")
        buf = fin.readline()
        tmp = []
        while buf != "" and buf != "no":
            try:
                if sizes == 1:
                    a, b, d = map(float, buf.split())
                    c = 0
                elif sizes == 2:
                    a, b, c, d = map(float, buf.split())
                else:
                    raise RuntimeError('Неправильная размерность аппроскимации (нужна 1 или 2)')
                tmp.append(TableLine())
                tmp[-1].set(a, b, c, d)
            except RuntimeError:
                print("Какую аппроксимацию мы проводим?")
                buf = "no"
            except Exception:
                print("Файл испорчен")
                buf = "no"
        fin.close()
        if buf == "":
            self.table = tmp

    def print(self):
        try:
            ptrb = ""
            if self.sizes == 1:
                prtb = "-" * 45 + '\n'
                prtb = prtb + "|{:^10s}|{:^10s}|{:^10s}|{:^10s}|\n".format("№", "X", "Y", "R")
                prtb = prtb + "-" * 45 + '\n'
                i = 1
                for elem in self.table:
                    prtb = prtb + "|{:^10d}|{:^10.3f}|{:^10.3f}|{:^10.3f}|\n".format(i, elem.x, elem.y, elem.r)
                    i += 1
                prtb = prtb + "-" * 45 + '\n'
                print(prtb)
            elif self.sizes == 2:
                prtb = "-" * 56 + '\n'
                prtb = prtb + "|{:^10s}|{:^10s}|{:^10s}|{:^10s}|{:^10s}|\n".format("№", "X", "Y", "Z", "R")
                prtb = prtb + "-" * 56 + '\n'
                i = 1
                for elem in self.table:
                    prtb = prtb + "|{:^10d}|{:^10.3f}|{:^10.3f}|{:^10.3f}|{:^10.3f}|\n".format(i, elem.x, elem.y, elem.z, elem.r)
                    i += 1
                prtb = prtb + "-" * 56 + '\n'
                print(prtb)
            else:
                raise RuntimeError('Неправильная размерность аппроскимации (нужна 1 или 2)')
        except RuntimeError:
            print("Какую аппроксимацию мы проводим?")

    def setWeight(self):
        tmp = self.table.copy()
        for i in range(len(tmp)):
            tmp[i].r = readFloat(0, 200)
        else:
            self.table = tmp

    def graphic(self):
        if self.sizes == 1:
            k1 = solve1(self.table, 1)
            k2 = solve1(self.table, 2)
            plt.grid(True)
            plt.xlabel("X-axis")
            plt.ylabel("Y-axis")
            x = []
            y = []
            for elem in self.table:
                x.append(elem.x)
                y.append(elem.y)
            plt.scatter(x, y, color = "blue")
            xa = np.linspace(x[0], x[-1], 100)      
            for k in (k1, k2):
                dim = np.shape(xa)
                ya = np.zeros(100)
                for i in range(dim[0]):
                    j = 0
                    for a in k:
                        ya[i] += a * xa[i] ** j
                        j += 1
                color = (rnd.random(), rnd.random(), rnd.random())
                plt.plot(xa, ya, color = color, label = "{}-мерный полином".format(len(k) - 1))
            plt.legend()
            plt.show()
        else:
            k = solve2(self.table)
            ax = plt.axes(projection="3d")
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            ax.set_zlabel("Z-axis")
            x = []
            y = []
            z = []
            for elem in self.table:
                x.append(elem.x)
                y.append(elem.y)
                z.append(elem.z)
            ax.scatter3D(x, y, z, color = "blue")
            ax.legend(["Init data"])
            xa, ya = np.meshgrid(np.linspace(np.min(x), np.max(x), 100), 
                               np.linspace(np.min(y), np.max(y), 100))

            k = solve2(self.table)
            za = k[0] + k[1] * xa + k[2] * ya
            ax.plot_surface(xa, ya, za, cmap = "viridis")
            plt.show()

    
class TableLine:
    def __init__(self):
        self.x = self.y = self.z = self.r = 0

    def set(self, a, b, c = 0, d = 1):
        self.x = a
        self.y = b
        self.z = c
        self.r = d

def func1(x):
    return x ** 2 - 5

def func2(x, y):
    return x ** 2 - y ** 3 + 4

def readNum(left, right):
    buf = input(f"Введите целое число в диапазоне от {left} до {right}: ")
    if buf == "":
        print("А ввод сегодня будет?")
        return left - 1
    try:
        buf = int(buf)
    except Exception:
        print("Сказано же было, что вводить можно ТОЛЬКО целое число!")
        return left - 1
    if buf < left or buf > right:
        print("Число не входит в допустимый диапазон!")
        return left - 1
    return buf

def readFloat(left, right):
    buf = input(f"Введите число в диапазоне от {left} до {right}: ")
    if buf == "":
        print("А ввод сегодня будет?")
        return left - 1
    try:
        buf = float(buf)
    except Exception:
        print("Сказано же было, что вводить можно ТОЛЬКО целое число!")
        return left - 1
    if buf < left or buf > right:
        print("Число не входит в допустимый диапазон!")
        return left - 1
    return buf

def solve1(table, power):
    dim = power + 1
    
    A = np.zeros((dim, dim))
    B = np.zeros((dim, 1))

    x = np.zeros((len(table)), "float")
    y = np.zeros((len(table)), "float")
    r = np.zeros((len(table)), "float")
    for i in range(len(table)):
        x[i] = table[i].x
        y[i] = table[i].y
        r[i] = table[i].r

    for i in range(dim):
        for j in range(dim):
            A[i, j] = np.sum((r * x) ** (i + j))

        B[i, 0] = np.sum(r * y * x ** i)

    K = solve(A, B)

    return K.reshape((dim, ))

def solve2(table):

    x = np.zeros((len(table)), "float")
    y = np.zeros((len(table)), "float")
    z = np.zeros((len(table)), "float")
    r = np.zeros((len(table)), "float")
    for i in range(len(table)):
        x[i] = table[i].x
        y[i] = table[i].y
        z[i] = table[i].z
        r[i] = table[i].r

    A = np.array([
            [
            np.sum(r),
            np.sum(r * x),
            np.sum(r * y)
            ],
            [
            np.sum(r * x),
            np.sum(r * x ** 2),
            np.sum(r * y * x)
            ],
            [
            np.sum(r * y),
            np.sum(r * x * y),
            np.sum(r * y ** 2)
            ]
        ])

    B = np.array([
            [np.sum(r * z)],
            [np.sum(r * z * x)],
            [np.sum(r * z * y)]
        ])

    K = solve(A, B)
    
    return K.reshape((3, ))