#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# via https://github.com/inconvergent/sand-glyphs

import matplotlib.pyplot as plt
from numpy             import concatenate
from numpy             import column_stack
from numpy             import linspace
from numpy.random      import randint
from numpy.random      import random
from numpy.random      import seed
from scipy.interpolate import splev
from scipy.interpolate import splprep


def random_coords(x_loc, x_stretch, y_loc, y_stretch, n):

    def n_coords(stretch, loc):
        return (random(n) * stretch) + loc

    xy = [n_coords(x_stretch, x_loc), n_coords(y_stretch(), y_loc)]
    return column_stack(xy)


def word_points( word_len, x_loc, x_stretch, y_loc, y_stretch, min_char_pts
               , max_char_pts):

    def coords_shift_x(mod):
        x_shift = mod + (mod * 1.5)
        return random_coords( x_loc + x_shift
                            , x_stretch
                            , y_loc
                            , y_stretch
                            , randint(min_char_pts, max_char_pts)
                            )

    return concatenate(list(map(coords_shift_x, range(word_len))))


def xy_to_coords(xy):
    return xy[:, 0], xy[:, 1]


def interp_points(x, y):
    tck, u = splprep([x, y], s=0)
    u_new  = linspace(u.min(), u.max(), 100)
    curve  = splev(u_new, tck, der=0)
    return curve


def smudge(mod):
    return ((random() - 0.5) * mod)


def interp_word(word_len, x_loc, y_loc, char_params):
    char_params['word_len'] = word_len
    char_params['x_loc']    = x_loc
    char_params['y_loc']    = y_loc

    xy    = word_points(**char_params)
    x, y  = xy_to_coords(xy)
    curve = interp_points(x, y)
    return x, y, curve


def plot_word(x, y, curve, ax, ax_params, points):
    if points:
        ax.scatter(x, y, **ax_params['point_params'])
    line_params = { key: ax_params['line_params'][key]()
                    for key in ax_params['line_params'].keys()
                  }
    ax.plot(curve[0], curve[1], **line_params)


def plot_line( ax, x_init, x_limit, word_gap, y_loc, y_smudge, min_word_len
             , max_word_len, char_params, ax_params, points):
    x = x_init()
    while x < x_limit:
        word_len = randint(min_word_len, max_word_len)
        plot_word( *interp_word( word_len
                               , x
                               , y_loc + smudge(y_smudge)
                               , char_params
                               )
                 , ax
                 , ax_params
                 , points
                 )
        x += (word_len * word_gap())


def plot_page( ax, n_lines, x_init, x_limit, word_gap, y_scale, y_smudge
             , min_word_len, max_word_len, char_params, ax_params, points):
    for i in range(n_lines):
        y_loc = i * y_scale
        plot_line( ax
                 , x_init
                 , x_limit
                 , word_gap
                 , y_loc
                 , y_smudge
                 , min_word_len
                 , max_word_len
                 , char_params
                 , ax_params
                 , points
                 )


def check_params(params):
    return ( (params['n_lines']   > 1)     # other things can still go wrong!
           & (params['n_lines']   < 1000)
           & (params['x_limit']   > 0)     # this is mostly to prevent inf
           & (params['x_limit']   < 1000)  # loops
           & (params['min_word_len'] > 1)
           & (params['max_word_len'] > params['min_word_len'])
           & (params['char_params']['min_char_pts'] > 1)
           & ( params['char_params']['max_char_pts']
             > params['char_params']['min_char_pts']
             )
           )


def plot_params(params, fig_params, filename):

    def init_plot(fig_params):
        fig, ax = plt.subplots(**fig_params)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')
        return fig, ax

    def save_plot(filename):
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

    _, ax = init_plot(fig_params)
    params['ax'] = ax
    plot_page(**params)
    save_plot(filename)


def main():
    seed(2)

    fig_params = { 'figsize': (5, 7.5)
                 , 'dpi'    : 125
                 }
    ax_params  = { 'point_params': { 'marker': 'o'
                                   , 'c'     : 'r'
                                   , 's'     : 1
                                   , 'alpha' : 0.175
                                   }
                 , 'line_params' : { 'c'     : lambda: str(random() * 0.3)
                                   , 'lw'    : lambda: (random() * 0.05) + 0.29
                                   }
                 }
    params     = { 'n_lines'     : 30
                 , 'x_init'      : lambda: random() * 3.5
                 , 'x_limit'     : 100
                 , 'word_gap'    : lambda: 3 + (random() * 0.5)
                 , 'y_scale'     : 6
                 , 'y_smudge'    : 1.8
                 , 'min_word_len': 2
                 , 'max_word_len': 7
                 , 'char_params' : { 'x_stretch': 1
                                   , 'y_stretch': lambda: 2 + (random() * 3)
                                   , 'min_char_pts': 2
                                   , 'max_char_pts': 10
                                   }
                 , 'ax_params'   : ax_params
                 , 'points'      : True
                 }

    if not check_params(params):
        raise ValueError('Bad value(s) in params.')
    else:
        plot_params(params, fig_params, 'tmp/inconv_words.png')


if __name__ == '__main__':
    main()
