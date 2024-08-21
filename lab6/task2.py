import math

def main():
    x, y = readFile("data2.txt")
    if x is not None:
        printTable(["x", "y", "1", "2", "3", "4", "5"], [x, y, diff(x, y), diffCenter(x, y), 
                                                         secondRunge(x, y), alignVars(x, y), diff2(x, y)])

def readFile(filename):
    x = []
    y = []
    try:
        fin = open(filename, "r")
        buf = fin.readline()
        while buf != "":
            buf = list(map(float, buf.split()))
            if len(buf) != 2:
                raise ValueError("Invalid line size")
            x.append(buf[0])
            y.append(buf[1])
            buf = fin.readline()
        fin.close()
        for i in range(1, len(x)):
            if x[i] <= x[i - 1]:
                raise ValueError("Invalid values")
            if i > 1:
                if math.fabs(x[i] - 2 * x[i - 1] + x[i - 2]) > 1e-5:
                    raise ValueError("Invalid values")
    except Exception:
        x = None
        y = None
        print("Error. File corrupted.")
    finally:
        return x, y

def diff(x, y):
    res = [0] * len(x)
    res[0] = None
    for i in range(1, len(x)):
        res[i] = (y[i] - y[i - 1]) / (x[i] - x[i - 1])
    return res

def diffCenter(x, y):
    res = [0] * len(x)
    res[0] = None
    for i in range(1, len(x) - 1):
        res[i] = (y[i + 1] - y[i - 1]) / (x[i + 1] - x[i - 1])
    res[-1] = None
    return res

def secondRunge(x, y):
    res = [0] * len(x)
    res[0] = None
    res[1] = None
    for i in range(2, len(x)):
        res[i] = 2 * (y[i] - y[i - 1]) / (x[i] - x[i - 1]) - (y[i] - y[i - 2]) / (x[i] - x[i - 2])
    return res

def alignVars(x, y):
    res = [0] * len(x)
    for i in range(len(x) - 1):
        res[i] = (math.log(y[i + 1]) - math.log(y[i])) / (math.log(x[i + 1]) - math.log(x[i])) * (y[i] / x[i])
    res[-1] = None
    return res

def diff2(x, y):
    res = [0] * len(x)
    res[0] = None
    for i in range(1, len(x) - 1):
        res[i] = (y[i + 1] - 2 * y[i] + y[i - 1]) / (((x[i + 1] - x[i - 1]) / 2) ** 2)
    res[-1] = None
    return res

def printTable(names, table):
    strline = "+" + len(names) * "-------+" + "\n"
    buffer = strline
    buffer = buffer + "|"
    for name in names:
        buffer = buffer + f"{name:^7s}|"
    buffer = buffer + "\n"
    buffer = buffer + strline
    for i in range(len(table[0])):
        buffer = buffer + '|'
        for j in range(len(table)):
            if table[j][i] is None:
                buffer = buffer + "   *   |"
            else:
                buffer = buffer + f"{table[j][i]:7.4f}|"
        buffer = buffer + "\n"
        buffer = buffer + strline
    print(buffer)

if __name__ == "__main__":
    main()