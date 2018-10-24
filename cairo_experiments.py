#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cairo
from numpy.random import random

# via https://pycairo.readthedocs.io/en/latest/reference/context.html?highlight=line_to


def rand_coords(n):
    return random(n)


if __name__ == '__main__':
    n       = 20
    width   = 512
    height  = 512
    x, y    = rand_coords(n), rand_coords(n)
    alphas  = sorted(random(n - 1))
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx     = cairo.Context(surface)
    ctx.scale(width, height)

    for i in range(n - 1):
        ctx.move_to(x[i], y[i])
        ctx.line_to(x[i + 1], y[i + 1])
        ctx.set_source_rgba(0, 0, 0, alphas[i])
        ctx.set_line_width(0.0025)
        ctx.stroke()

    surface.write_to_png('tmp/cairo_experiments.png')
