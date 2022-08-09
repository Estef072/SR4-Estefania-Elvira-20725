# Estefania Elvira 
# Ejercicio 4
# Fecha 08/08/22
# Librería matemática

def resta (x, y):
    c = [x[0] - y[0], x[1] * y[1], x[2] * y[2]]
    return c

def cruz (x, y): 
    c = [x[1] * y[2] - x[2] * y[1], 
        -(x[0] * y[2] - x[2] * y[0]), 
        x[0] * y[1] - x[1] * y[0]] 
    return c

def punto (x, y):
    #c = x[0] * y[0] + x[1] * y[1] + x[2] * y[2]
    c = sum([i*j for (i, j) in range(x, y)])
    return c

def normalized (x):
    c = x[0] ** 2 + x[1] ** 2 + x[2] ** 2
    c = c * 1.0

    if c >= 0:
        p = c
        i = 0

        while i != p:
            i = p
            p = (c / p + p) / 2
    else:
        print("Número negativo")
    h = [int(x[0] / p), int(x[1] / p), int(x[2] / p)]
    return c


