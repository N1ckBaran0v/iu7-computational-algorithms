from os import system
from table import Table, readNum
from scipy.special import erfi
from scipy.linalg import solve
import sys
import numpy as np
import matplotlib.pyplot as plt
import math

def main():
    table = Table()
    table.sizes = 1
    menuPattern = """
Действия:
0. Выход.
1. Сгенерировать таблицу.
2. Задать веса.
3. Вывести таблицу.
4. Вывести график.
5. Вывести решение ДУ.
6. Сменить размерность аппроксимации."""
    while True:
        system("clear")
        menuText = menuPattern
        if table.sizes == 0:
            menuText = "Размерность аппроксимации не выбрана." +  menuText
        elif table.sizes == 1:
            menuText = "Аппроксимация одномерная." +  menuText
        elif table.sizes == 2:
            menuText = "Двумерная одномерная." +  menuText
        else:
            printf("Клоун, ты как таблицу сломал?")
            sys.exit(0)
        print(menuText)
        act = readNum(0, 7)
        match act:
            case 0:
                print("До свидания!")
                break
            case 1:
                table.generate()
            case 2:
                table.setWeight()
            case 3:
                table.print()
            case 4:
                table.graphic()
            case 5:
                solveur()
            case 6:
                table.setSizes(table.sizes % 2 + 1)
            case _:
                pass
        input("Нажмите Enter, чтобы продолжить:")





def difffunc(x):
    return (math.exp(-x**2/2) * ((1 + math.exp(x**2/2) * x) * erfi(1/math.sqrt(2)) - (1 + math.sqrt(math.e)) * erfi(x/math.sqrt(2))))/erfi(1/math.sqrt(2))

def solveur():
    x0 = -0.5
    xn = 2
    n = 10

    x = np.linspace(x0, xn, n)
    y = np.array([difffunc(xi) for xi in x])

    # m = 2

    a = -2 + 2 * x - 3 * x ** 2
    b = 2 - 6 * x + 3 * x ** 2 - 4 * x ** 3
    ab = a * b
    
    kA = np.array([[np.sum(a ** 2), np.sum(ab)],
                       [np.sum(ab), np.sum(b ** 2)]])
   
    sum1 = a * (4 * x - 1)
    sum2 = b * (4 * x - 1)
    
    kB = np.array([[np.sum(sum1)],
                   [np.sum(sum2)]])
    
    kX2 = solve(kA, kB).reshape((2, ))

    y2 = getPolynom(x, 2, kX2)

    # m = 3

    g = 6 * x - 12 * x ** 2 + 4 * x ** 3 - 5 * x ** 4
    ag = a * g
    bg = b * g

    kA = np.array([[np.sum(a** 2), np.sum(ab), np.sum(ag)],
                       [np.sum(ab), np.sum(b ** 2), np.sum(bg)],
                       [np.sum(ag), np.sum(bg), np.sum(g ** 2)]])
    
    sum3 = g * (4 * x - 1)
    
    kB = np.array([[np.sum(sum1)],
                       [np.sum(sum2)],
                       [np.sum(sum3)]])

    kX3 = solve(kA, kB).reshape((3, ))

    y3 = getPolynom(x, 3, kX3)

    plt.grid(True)

    plt.plot(x, y2, color = "blue", label = "m = 2")
    plt.plot(x, y3, color = "red", label = "m = 3")
    plt.plot(x, y, color = "green", label = "Init func")

    plt.legend()

    plt.show()

def getPolynom(x, n: int, koefs: list):

    if n == 2:
        return 1 - x + koefs[0] * x * (1 - x) + koefs[1] * x ** 2 * (1 - x)
    else:
        return 1 - x + koefs[0] * x * (1 - x) + koefs[1] * x ** 2 * (1 - x) + koefs[2] * x ** 3 * (1 - x)

if __name__  == "__main__":
    main()