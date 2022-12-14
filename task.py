from sympy import parse_expr, fourier_series, latex
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application, convert_xor
import matplotlib.pyplot as plt
import numpy as np

transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))


def latex_fourier_series(function, variable, order, point):
    series = calculate_fourier_series(function, variable, order, point)
    return latex(series)


def draw_plot(function, variable, order, point):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    x = np.linspace(*[float(e.evalf()) for e in point], 100)

    plt.plot(x, [function.subs(variable, x) for x in x], '#1e2761')

    s = calculate_fourier_series(function, variable, order, point)
    plt.plot(x, [s.subs(variable, x) for x in x], '#7a2048')

    ax.grid(which='major', color='#bbb', linewidth=0.8)
    ax.grid(which='minor', color='#bbb', linestyle=':', linewidth=0.5)
    ax.minorticks_on()
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend(['Исходная функция', 'Ряд Фурье'])

    return fig


def calculate_fourier_series(function, variable, order, point):
    s = fourier_series(function, (variable, point[0], point[1]))
    terms = s.truncate(order)
    return terms


def parse_function(expression):
    try:
        f = parse_expr(expression, transformations=transformations)
        variables = list(f.free_symbols)
        if len(variables) != 1:
            return None
        return f, variables[0]
    except:
        return None


def parse_number(expression):
    try:
        f = parse_expr(expression, transformations=transformations)
        if len(f.free_symbols) != 0:
            return None
        return f
    except:
        return None
