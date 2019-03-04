from app import App
from math import pow, e, asin

if __name__ == '__main__':
    functions = dict([
        ('1', lambda x, a, b, c: (x**2 - a**2)/(x**2 - b*x - c)),
        ('2', lambda x, a, b, c: a*x**4/(b + x)**3),
        ('3', lambda x, a, b, c: a*x/((b + x)*(c - x)**2)),
        ('4', lambda x, a, b, c: ((a + x)/(b - x))**4),
        ('5', lambda x, a, b, c: a*x/(b - x*x*x)**2),
        ('6', lambda x, a, b, c: a*x**2/pow(x**2 - b**2, 1/3)),
        ('7', lambda x, a, b, c: (a*x**2/(x + b))**(1/3)),
        ('8', lambda x, a, b, c: a*e**x/(b + x)),
        ('9', lambda x, a, b, c: asin(a)*x/(b**2 - x**2)**.5),
        ('10', lambda x, a, b, c: a - x + (x**3/(b + x))**.5)
    ])

    app = App(functions)
    app.mainloop()
