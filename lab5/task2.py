import math

def main():
    x = float(input("Введите Ф(x): "))
    if x > 0 and x < 1:
        print(f"Ответ: {find(x):.5f}")
    else:
        print("Ошибка. Значение функции Лапласа должно лежать в интервале (0, 1).")

def PHI(x):
    ans = 0
    step = x / 100
    itstep = step * 2
    x0 = 0.0
    while x0 < x:
        ans += math.exp((-1 * (x0 ** 2)) / 2) + 4 * math.exp((-1 * ((x0 + step) ** 2)) / 2) + math.exp((-1 * ((x0 + itstep) ** 2)) / 2)
        x0 += itstep
    return (2 / math.sqrt(2 * math.pi)) * (step / 3) * ans    

def find(phi):
    maxsteps = 1000
    minval = 0
    maxval = 4
    while maxval - minval > 1e-7 and maxsteps > 0:
        tmp = (maxval + minval) / 2
        if phi <= PHI(tmp):
            maxval = tmp
        else:
            minval = tmp
        maxsteps -= 1
    return minval

if __name__ == "__main__":
    main()