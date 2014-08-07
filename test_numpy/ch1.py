import sys
from datetime import datetime
import numpy as np


def pythonsum(n):
    a = range(n)
    b = range(n)
    c = []
    for i in range(len(a)):
        a[i] = i ** 2
        b[i] = i ** 3
        c.append(a[i] + b[i])
    return c


def numpysum(n):
    a = np.arange(n) ** 2
    b = np.arange(n) ** 3
    c = a + b
    return c


if __name__ == '__main__':

    for size in [10000L, 100000L, 1000000L]:
        start = datetime.now()
        c = pythonsum(size)
        delta = datetime.now() - start
        print('SIZE:{}\tLAST_ONE:{}\tTIME:{}ms'.format(size, c[-1:], delta))

        start = datetime.now()
        c = numpysum(size)
        delta = datetime.now() - start
        print('SIZE:{}\tLAST_ONE:{}\tTIME:{}ms'.format(size, c[-1:], delta))

        print('=' * 80)
