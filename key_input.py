#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
from time import sleep


def update(window, x, y, char):
    window.addch(x, y, char)
    window.refresh()


def adjust_xy(x, y, move, max_yx):
    x_max , y_max  = max_yx
    x_move, y_move = move
    new_x = check_move(x, x_move, 0, x_max)
    new_y = check_move(y, y_move, 1, y_max - 1)
    return new_x, new_y


def check_move(coord, move, dim_min, dim_max):
    new_coord = coord + move
    if (new_coord < dim_max) & (new_coord >= dim_min):
        return new_coord
    elif coord > dim_max:
        return dim_max - 1
    else:
        return coord


def check_onscreen(x, y, max_yx):
    x_max, y_max = max_yx
    return not ((x >= x_max) | (y > y_max))


def loop(window):

    def print_line(ik):
        i, k = ik
        window.addstr(i, 0, k)

    window.keypad(True)
    curses.curs_set(0)
    window.nodelay(True)

    move_dict = { curses.KEY_UP   : (-1,  0)
                , curses.KEY_DOWN : ( 1,  0)
                , curses.KEY_LEFT : ( 0, -1)
                , curses.KEY_RIGHT: ( 0,  1)
                }

    refresh = round(1 / 60, 4)
    key     = ''
    char    = '*'
    x, y    = (20, 50)
    max_yx  = window.getmaxyx()
    ticker  = 0

    update(window, x, y, char)

    while key != ord('q'):
        max_yx = window.getmaxyx()

        if ticker == 0:
            infos = [ '"q" to quit'
                    , 'window size: ' + str(max_yx)
                    , 'curses.KEY : ' + str(key)
                    ]
            list(map(print_line, enumerate(infos)))
            window.refresh()

        if key in move_dict.keys():
            if check_onscreen(x, y, max_yx):
                update(window, x, y, ' ')
            x, y, = adjust_xy(x, y, move_dict[key], max_yx)
            update(window, x, y, char)

        sleep(0.01)
        key = window.getch()

        if ticker < 30:
            ticker += 1
        else:
            ticker = 0


def main():
    curses.wrapper(loop)


if __name__ == '__main__':
    main()
