#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
from time import sleep


def spin(i, n):
    spin_series = ['|', '/', '--', '\\']
    spin_map    = {i: spin_series[i] for i in range(len(spin_series))}
    char_map    = {0: spin_map[i % len(spin_map)]}

    for k in range(1, n):
        char_map[k] = '_'

    char_spin = ''
    for j in range(n):
        char_spin += char_map[(i + (n - j)) % len(char_map.keys())]

    return char_spin


def spin_window(window):
    curses.curs_set(0)
    window.nodelay(True)

    n = 40
    i = 0
    while True:
        window.addstr(4, 4, spin(i, n))
        window.refresh()
        i += 1
        sleep(0.05)


def main():
    curses.wrapper(spin_window)


if __name__ == '__main__':
    main()
