#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# via https://github.com/inconvergent/sand-glyphs

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


def smudge(mod):
    return ((random() - 0.5) * mod)


def main():

    def chain_to_plot(ax, chain_len, x_loc, y_loc):
        params = {'x_stretch': 1, 'y_stretch': 3, 'min_n': 3, 'max_n': 7}
        params['chain_len'] = chain_len
        params['x_loc']     = x_loc
        params['y_loc']     = y_loc

        xy     = word_chain(**params)
        x, y   = xy_to_coords(xy)
        curve  = interpolate_points(x, y)

        draw_word(ax, x, y, curve, True)

    def chain_words(y_loc, x_limit):

        def spacing_scale(x_pos):
            return (x_pos * (3 + (random() * 0.5)))

        x = random() * 3.5
        while x < x_limit:
            chain_len = randint(2, 7)
            chain_to_plot(ax, chain_len, x, y_loc + smudge(0.35))
            x += spacing_scale(chain_len)

    def write_lines(n_lines, y_scale, x_limit):
        for i in range(n_lines):
            y = i * y_scale
            chain_words(y, x_limit)

    def init_plot():
        fig, ax = plt.subplots(figsize=(5, 6))
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        return fig, ax

    def save_plot():
        plt.tight_layout()
        plt.savefig('inconv_words.png')
        plt.close()

    def draw_word(ax, x, y, curve, points=False):
        if points:
            ax.plot(x, y, 'ro', ms=1, alpha=0.175)
        ax.plot(curve[0], curve[1], c='k', lw=0.325)

    seed(2)
    _, ax = init_plot()
    write_lines(n_lines=35, y_scale=5, x_limit=100)
    save_plot()


if __name__ == '__main__':
    main()
