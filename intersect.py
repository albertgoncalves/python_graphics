#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# via https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/


def point(x, y):
    return {'x': x, 'y': y}


def f_ax(f):
    return lambda ax: lambda k, l: f(k[ax], l[ax])


def subtr_ax(ax):
    return f_ax(lambda i, j: i - j)(ax)


def ccw(a, b, c):
    return ( (subtr_ax('y')(c, a) * subtr_ax('x')(b, a))
           > (subtr_ax('y')(b, a) * subtr_ax('x')(c, a))
           )


def intersect(a, b, c, d):
    return (ccw(a, c, d) != ccw(b, c, d)) & (ccw(a, b, c) != ccw(a, b, d))


def main():
    a = point(0, 0)
    b = point(0, 1)
    c = point(1, 1)
    d = point(1, 0)

    print(intersect(a, b, c, d))
    print(intersect(a, c, b, d))
    print(intersect(a, d, b, c))


if __name__ == '__main__':
    main()
