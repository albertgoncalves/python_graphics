#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import floor

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


def init_page(width, height):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx     = cairo.Context(surface)

    ctx.rectangle(0, 0, width, height)
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)

    return surface, ctx



def word_pts(k, l, n_pts, w_len, rand_x, rand_y, rand_z):
    x, y, z = [], [], []
    nn      = 0
    for i in range(w_len()):
        n = n_pts()
        x.extend(rand_x(n, i, k))
        y.extend(rand_y(n, l))
        z.extend(rand_z(n))
        nn += n

    return x, y, z, nn


def interp_points(x, y, z, nn, res):
    tck, u = splprep([x, y, z], s=0)
    u_new  = linspace(u.min(), u.max(), nn * res)
    curve  = splev(u_new, tck, der=0)
    return curve


def lines_init(width, height, pad, scale, lw, char_params):
    return lambda k, l: word_pts(k, l, **char_params)


def interp_words(lines, res, limit, ls, h_gap, v_gap):
    rows = []
    for l in range(ls):
        row = []
        k   = 0

        while True:
            row.append(interp_points(*lines(k * h_gap(), l * v_gap()), res))
            k += 1
            if min(row[-1][0]) > limit:
                break

        rows.extend(row)

    return rows


def plot_lines(ctx):
    def for_xyz(x, y, z):
        for i in range(len(x) - 1):
            ctx.move_to(x[i], y[i])
            ctx.line_to(x[i + 1], y[i + 1])
            ctx.set_line_width(z[i])
            ctx.set_source_rgb(0, 0, 0)
            ctx.stroke()

    return for_xyz


def main():
    seed(1)
    m      = 1.15
    width  = floor(m * 475)
    height = floor(m * 590)
    pad    = floor(m * 50)
    res    = 25
    scale  = 9
    lw     = 1.1

    char_params = { 'n_pts' : lambda        : poisson(0.1) + 2
                  , 'w_len' : lambda        : poisson(1.75) + 2
                  , 'rand_x': lambda n, i, k: ( scale
                                              * (random(n) + i + k)
                                              ) + pad
                  , 'rand_y': lambda n, l   : ( scale
                                              * ( beta(1.5, 1.75, size=n)
                                                + l
                                                + beta(1.25, 1.25) - 0.5
                                                )
                                              * 0.975
                                              ) + pad
                  , 'rand_z': lambda n      : lw * beta(4, 5, size=n)
                  }
    line_params = { 'limit' : width - (pad * 2.35)
                  , 'ls'    : floor(m * 19)
                  , 'h_gap' : lambda: uniform(3.75, 3.8)
                  , 'v_gap' : lambda: uniform(3.05, 3.1)
                  }

    lines = lines_init(width, height, pad, scale, lw, char_params)
    xyzs  = interp_words(lines, res, **line_params)

    surface, ctx = init_page(width, height)
    for xyz in xyzs:
        plot_lines(ctx)(*xyz)

    surface.write_to_png('tmp/cairo_experiments.png')


if __name__ == '__main__':
    main()
