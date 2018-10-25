#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cairo

from numpy             import linspace
from numpy.random      import random
from numpy.random      import randint
from numpy.random      import poisson
from scipy.interpolate import splev
from scipy.interpolate import splprep

# via https://pycairo.readthedocs.io/en/latest/reference/context.html?highlight=line_to


def rand_coords(n):
    return (random(n) * 0.5) + 0.25


def interp_points(x, y, resolution=300):
    tck, u = splprep([x, y], s=0)
    u_new  = linspace(u.min(), u.max(), resolution)
    curve  = splev(u_new, tck, der=0)
    return curve


def word_pts(fn, wlen, scale, pad):
    x, y = [], []
    for i in range(wlen):
        n = fn()
        x.extend((scale * (random(n) + i  )) + pad)
        y.extend((scale * (random(n) + 0.5)) + pad)

    return x, y


def rev(arr):
    return arr[::-1]


def main():
    n       = 5
    width   = 1000
    height  = 400
    scale   = (width + height) / 10
    pad     = 50
    res     = 1000
    pts     = word_pts(lambda: poisson(0.9) + 2, randint(5, 7), scale, pad)
    x, y    = interp_points(*pts, res)
    # alphas  = rev(sorted(random(res - 1)))
    # lws     = rev(sorted(random(res - 1) * 5))
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx     = cairo.Context(surface)
    # ctx.scale(width, height)
    ctx.rectangle(0, 0, width, height)
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()

    for i in range(res - 1):
        ctx.move_to(x[i], y[i])
        ctx.line_to(x[i + 1], y[i + 1])
        # ctx.set_source_rgba(0, 0, 0, alphas[i])
        # ctx.set_line_width(lws[i])
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(1)
        ctx.stroke()

    surface.write_to_png('tmp/cairo_experiments.png')


if __name__ == '__main__':
    main()
