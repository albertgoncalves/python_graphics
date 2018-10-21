#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy             import concatenate
from numpy             import column_stack
from numpy             import cos
from numpy             import linspace
from numpy             import pi
from numpy             import sin
from numpy.random      import randint
from numpy.random      import random
from numpy.random      import seed
from numpy.random      import shuffle
from scipy.interpolate import splev
from scipy.interpolate import splprep


def random_coords(x_loc, x_stretch, y_loc, y_stretch, n):

    def prepare_coord(stretch, loc, n):
        return (random(n) * stretch) + loc

    x = prepare_coord(x_stretch, x_loc, n)
    y = prepare_coord(y_stretch, y_loc, n)

    return column_stack([x, y])


def word_chain(chain_len, x_loc, x_stretch, y_loc, y_stretch, min_n, max_n):

    def rand_n(min_n, max_n):
        return randint(min_n, max_n, 1)

    def coords_shift_x(mod):
        x_shift = mod + (mod * 1.5)

        return random_coords( x_loc + x_shift
                            , x_stretch
                            , y_loc
                            , y_stretch
                            , rand_n(min_n, max_n)
                            )

    return concatenate(list(map(coords_shift_x, range(chain_len))))


def xy_to_coords(xy):
    return xy[:, 0], xy[:, 1]


def interpolate_points(x, y):
    tck, u = splprep([x, y], s=0)
    u_new  = linspace(u.min(), u.max(), 1000)
    curve  = splev(u_new, tck, der=0)
    return curve


def main():

    def init_plot():
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        return fig, ax

    def show_plot():
        plt.tight_layout()
        plt.show()

    def draw_words(ax, x, y, curve):
        ax.plot(x, y, 'ro')
        ax.plot(curve[0], curve[1], 'k-')

    seed(5)
    params = {'x_stretch': 1, 'y_stretch': 5, 'min_n': 3, 'max_n': 6}
    xy     = word_chain(chain_len=3, x_loc=0, y_loc=1, **params)
    x, y   = xy_to_coords(xy)
    curve  = interpolate_points(x, y)

    _, ax = init_plot()
    draw_words(ax, x, y, curve)
    show_plot()


if __name__ == '__main__':
    main()
