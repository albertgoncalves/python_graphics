#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sig_btwn_pts(x, y1, y2, v):
    y   = y2 - y1
    ys2 = (sigmoid(x) * y) + y1
    ys1 = ys2 + v

    return ys1, ys2


def list_to_elements(dict_items):
    values      = [np.abs(v) for v in list(dict_items.values())]
    n           = len(values)
    total       = np.sum(values)
    gap         = total * 0.05
    labels      = list(dict_items.keys())
    right_edges = [0] + np.cumsum(values[:-1]).tolist()
    left_edges  = [ l + (i * gap) - (total / n)
                    for i, l in enumerate(right_edges)
                  ]

    return values, left_edges, right_edges, labels, total


def gen_x(m):  # slope of curves
    return np.linspace(-m, m, 100)


def get_margins():
    return (0.025, -0.045, 0.915, 1.025)  # left, bottom, right, top


def usd(num_value):
    return '${:,.2f}'.format(num_value)


def chart_from_elements(values, left_edges, right_edges, labels, total, m):
    x     = gen_x(m)
    x_min = np.min(x)
    x_max = np.max(x)

    fig, ax = plt.subplots(figsize=(6, 6))

    for v, le, re, lb in zip(values, left_edges, right_edges, labels):
        ax.fill_between(x, *sig_btwn_pts(x, le, re, v))
        ax.text( x_min - 0.25
               , (le + (v / 2))
               , '\n'.join([lb, usd(v)])
               , ha      ='right'
               , va      ='center'
               , fontsize='small'
               )

    ax.text(x_max + 0.25, total / 2, usd(total), fontsize='large')
    rect = Rectangle((x_max, 0), -0.5, total, alpha=0.5, color='w')
    ax.add_patch(rect)

    ax.axis('off')

    plt.tight_layout(rect=get_margins())
    plt.savefig('tmp/sankey_demo.png')
    plt.close()


def sort_data(data):
    return dict(sorted(data.items(), key=lambda kv: kv[1]))


def make_sankey(data, slope):
    return chart_from_elements(*list_to_elements(sort_data(data)), slope)


if __name__ == '__main__':
    slope = 6
    data  = { 'Aaaa'     : 25
            , '&&\nlr'   : 185
            , 'Big G'    : 100.01
            , 'Bernar'   : 4.99
            , 'Cpt. Phel': 150.5
            , 'GI JOE'   : 99
            , '1\n2\n3'  : 123
            }

    make_sankey(data, slope)
