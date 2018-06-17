#!/usr/bin/python

import sys

from labrat.math import dilute_stock


def load_literal(lit):
    if '.' in lit:
        return float(lit)
    return int(lit)


if __name__ == '__main__':
    if sys.argv[0] != 'python3':
        print('Usage: python3 labrat.py FUNCTION [arg1] ... [argk1=argv1] ...')
        sys.exit(1)
    argl = list()
    argd = dict()
    for v in sys.argv:
        if '=' in v:
            key, value = v.split('=')
            argd[key] = load_literal(value)
        else:
            argl.append(load_literal(v))
    if argl[1] == 'dilute_stock':
        res = dilute_stock(argl[2], argl[3], **argd)
    print(res)
