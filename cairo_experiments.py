#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cairo

from numpy             import linspace
from numpy.random      import beta
from numpy.random      import random
from numpy.random      import randint
from numpy.random      import poisson
from numpy.random      import seed
from numpy.random      import uniform
from scipy.interpolate import splev
from scipy.interpolate import splprep

# via https://pycairo.readthedocs.io/en/latest/reference/context.html?highlight=line_to


def interp_points(x, y, z, res):
    tck, u = splprep([x, y, z], s=0)
    u_new  = linspace(u.min(), u.max(), res)
    curve  = splev(u_new, tck, der=0)
    return curve


def init_page(width, height):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx     = cairo.Context(surface)

    ctx.rectangle(0, 0, width, height)
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)

    return surface, ctx



def plot_lines(ctx, res):
    def for_xyz(x, y, z):
        for i in range(res - 1):
            ctx.move_to(x[i], y[i])
            ctx.line_to(x[i + 1], y[i + 1])
            ctx.set_line_width(z[i])
            ctx.set_source_rgb(0, 0, 0)
            ctx.stroke()

    return for_xyz


def word_pts(k, l, n_pts, w_len, rand_x, rand_y, rand_z):
    x, y, z = [], [], []
    for i in range(w_len()):
        n = n_pts()
        x.extend(rand_x(n, i, k))
        y.extend(rand_y(n, l))
        z.extend(rand_z(n))

    return x, y, z


def lines_init(width, height, pad, scale, lw, char_params):
    return lambda k, l: word_pts(k, l, **char_params)


def interp_words(lines, res, limit, ls, h_gap, v_gap):

    def max_x(row, limit):
        if len(row) > 0:
            if max(row[-1][0]) < limit:
                return True
            else:
                return False
        else:
            return True

    rows = []
    for l in range(ls()):
        row = []
        k   = 0
        while max_x(row, limit):
            row.append(interp_points(*lines(k * h_gap(), l * v_gap()), res))
            k += 1
        rows.extend(row)

    return rows

def main():
    seed(1)
    width   = 1000
    height  = 500
    res     = 1000
    pad     = 35
    scale   = 10
    lw      = scale / 40

    char_params = { 'n_pts' : lambda        : poisson(0.9) + 2
                  , 'w_len' : lambda        : randint(5, 7)
                  , 'rand_x': lambda n, i, k: ( scale
                                              * (random(n)  + i + k)
                                              ) + pad
                  , 'rand_y': lambda n, l   : ( scale
                                              * (random(n)  + l)
                                              ) + pad
                  , 'rand_z': lambda n      : (lw    *  random(n)) + 0.5
                  }
    line_params = { 'limit': width - (pad * 2)
                  , 'ls'   : lambda: 8
                  , 'h_gap': lambda: uniform(5, 7)
                  , 'v_gap': lambda: uniform(3.5, 4)
                  }

    lines = lines_init(width, height, pad, scale, lw, char_params)
    xyzs  = interp_words(lines, res, **line_params)

    surface, ctx = init_page(width, height)
    for xyz in xyzs:
        plot_lines(ctx, res)(*xyz)

    surface.write_to_png('tmp/cairo_experiments.png')


if __name__ == '__main__':
    main()
