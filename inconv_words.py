#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# via https://github.com/inconvergent/sand-glyphs

import matplotlib.pyplot as plt
from numpy             import concatenate
from numpy             import column_stack
from numpy             import linspace
from numpy.random      import normal
from numpy.random      import random
from numpy.random      import poisson
from numpy.random      import seed
from numpy.random      import uniform
from scipy.interpolate import splev
from scipy.interpolate import splprep


def random_coords(x_loc, x_stretch, y_loc, y_stretch, n):

    def n_coords(stretch, loc):
        return (random(n) * stretch) + loc

    xy = [n_coords(x_stretch, x_loc), n_coords(y_stretch(), y_loc)]
    return column_stack(xy)


def word_points( word_len, x_loc, x_stretch, x_spread, y_loc, y_stretch
               , n_char_pts):

    def coords_shift_x(x_pos):
        x_shift = x_spread(x_pos)
        return random_coords( x_loc + x_shift
                            , x_stretch
                            , y_loc
                            , y_stretch
                            , n_char_pts()
                            )

    return concatenate(list(map(coords_shift_x, range(word_len))))


def xy_to_coords(xy):
    return xy[:, 0], xy[:, 1]


def interp_points(x, y, resolution=300):
    tck, u = splprep([x, y], s=0)
    u_new  = linspace(u.min(), u.max(), resolution)
    curve  = splev(u_new, tck, der=0)
    return curve


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


def plot_line( ax, x_init, x_limit, word_gap, y_loc, y_smudge, n_word_len
             , char_params, ax_params, points):
    x = x_init()
    while x < x_limit:
        word_len = n_word_len()
        plot_word( *interp_word( word_len
                               , x
                               , y_loc + y_smudge()
                               , char_params
                               )
                 , ax
                 , ax_params
                 , points
                 )
        x += (word_len * word_gap())


def plot_page( ax, n_lines, x_init, x_limit, word_gap, y_scale, y_smudge
             , n_word_len, char_params, ax_params, points):
    for i in range(n_lines):
        y_loc = i * y_scale
        plot_line( ax
                 , x_init
                 , x_limit
                 , word_gap
                 , y_loc
                 , y_smudge
                 , n_word_len
                 , char_params
                 , ax_params
                 , points
                 )


def check_params(params):
    return ( (params['n_lines'] > 1)     # other things can still go wrong!
           & (params['n_lines'] < 1000)
           & (params['x_limit'] > 5)     # this is mostly to prevent inf
           & (params['x_limit'] < 1000)  # loops
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

    fig_params   = { 'figsize'     : (3, 3.65)
                   , 'dpi'         : 150
                   }
    point_params = { 'marker'      : 'o'
                   , 'c'           : 'r'
                   , 's'           : 0.25
                   , 'alpha'       : 0.1
                   }
    line_params  = { 'c'           : lambda: str(uniform(0, 0.25))
                   , 'lw'          : lambda: uniform(0.285, 0.35)
                   }
    ax_params    = { 'point_params': point_params
                   , 'line_params' : line_params
                   }
    char_params  = { 'x_stretch'   : 1.25
                   , 'x_spread'    : lambda x: x * uniform(1.65, 2.65)
                   , 'y_stretch'   : lambda: uniform(0.7, 3.7)
                   , 'n_char_pts'  : lambda: poisson(0.75) + 2
                   }
    params       = { 'n_lines'     : 21
                   , 'x_init'      : lambda: uniform(0, 3.5)
                   , 'x_limit'     : 100
                   , 'word_gap'    : lambda: uniform(2.5, 3)
                   , 'y_scale'     : 7
                   , 'y_smudge'    : lambda: normal(0, 0.25)
                   , 'n_word_len'  : lambda: poisson(3) + 2
                   , 'char_params' : char_params
                   , 'ax_params'   : ax_params
                   , 'points'      : False
                   }

    if not check_params(params):
        raise ValueError('Bad value(s) in params.')
    else:
        plot_params(params, fig_params, 'tmp/inconv_words.png')


if __name__ == '__main__':
    main()
