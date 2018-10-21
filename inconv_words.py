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


def char_chain(chain_len, x_loc, x_stretch, y_loc, y_stretch, min_n, max_n):

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


def chain_to_plot(ax, chain_len, x_loc, y_loc, subparams):
    subparams['chain_len'] = chain_len
    subparams['x_loc']     = x_loc
    subparams['y_loc']     = y_loc

    xy    = char_chain(**subparams)
    x, y  = xy_to_coords(xy)
    curve = interpolate_points(x, y)

    draw_word(ax, x, y, curve, points=True)


def chain_words( ax, x_init, x_limit, word_gap, y_loc, y_smudge, min_chain
               , max_chain, subparams):

    x = x_init()
    while x < x_limit:
        chain_len = randint(min_chain, max_chain)
        chain_to_plot( ax
                     , chain_len
                     , x, y_loc + smudge(y_smudge)
                     , subparams
                     )
        x += (chain_len * word_gap())


def write_lines( ax, n_lines, x_init, x_limit, word_gap, y_scale, y_smudge
               , min_chain, max_chain, subparams):
    for i in range(n_lines):
        y_loc = i * y_scale
        chain_words( ax
                   , x_init
                   , x_limit
                   , word_gap
                   , y_loc
                   , y_smudge
                   , min_chain
                   , max_chain
                   , subparams
                   )


def draw_word(ax, x, y, curve, points=False):
    if points:
        ax.plot(x, y, 'ro', ms=1, alpha=0.175)
    ax.plot(curve[0], curve[1], c='k', lw=0.325)


def main():

    def plot_params(params, fig_params, filename):

        def init_plot(fig_params):
            fig, ax = plt.subplots(**fig_params)
            ax.set_aspect('equal')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.axis('off')
            return fig, ax

        def save_plot():
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()

        _, ax = init_plot(fig_params)
        params['ax'] = ax
        write_lines(**params)
        save_plot()

    seed(2)
    fig_params = { 'figsize'  : (5, 6.5)
                 , 'dpi'      : 115
                 }
    params     = { 'n_lines'  : 30
                 , 'x_init'   : lambda: random() * 3.5
                 , 'x_limit'  : 100
                 , 'word_gap' : lambda: (3 + (random() * 0.5))
                 , 'y_scale'  : 5.15
                 , 'y_smudge' : 0.35
                 , 'min_chain': 2
                 , 'max_chain': 7
                 , 'subparams': { 'x_stretch': 1
                                , 'y_stretch': 2.5
                                , 'min_n'    : 2
                                , 'max_n'    : 10
                                }
                 }

    plot_params(params, fig_params, 'inconv_words.png')


if __name__ == '__main__':
    main()
