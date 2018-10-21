#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
# from functools import reduce
import random
from time import sleep


def random_cursor(max_x, max_y):

    def random_between(min_val):
        return lambda max_val: random.randint(min_val, max_val - 1)

    return tuple(map(random_between(0), [max_x, max_y]))


def flip_2(tuple_2):
    y, x = tuple_2
    return x, y


def pad(string, n=4):
    return string + (' ' * n)


def loading_bar(n, i):
    return '[' + ('=' * i) + '>' + (' ' * (n - i)) + ']'


def int_char_length(int_val):
    return len(str(int_val))


# def max_list(list_eq):
#     return reduce((lambda x, y: max(x, y)), list_eq)


def insert_format(str_format):
    return '{' + str_format + '}'


def assemble_xy_format(str_format):
    return insert_format(str_format) + ', ' + insert_format(str_format)


def output_formats(format_len):
    output_format = assemble_xy_format(':>' + str(format_len))
    window_output = 'window size: ' + output_format
    cursor_output = 'cursor pos : ' + output_format

    return window_output, cursor_output


def pbar(window):
    char_map = {0: '-', 1: '\\', 2: '|', 3: '/'}
    n, k = (80, 4)

    for i in range(n):
        max_x, max_y = flip_2(window.getmaxyx())
        new_x, new_y = random_cursor(max_x, max_y)
        current_char = char_map[i % len(char_map.keys())]

        format_len = max(list(map(int_char_length, [max_x, max_y])))
        window_output, cursor_output = output_formats(format_len)

        window.addstr(0, k - 1, pad(loading_bar(n, i)))
        window.addstr(1, 0,     current_char)
        window.addstr(1, k + i, current_char)
        window.addstr(3, 0, pad(window_output.format(max_x, max_y)))
        window.addstr(4, 0, pad(cursor_output.format(new_x, new_y)))
        window.addstr(new_y, new_x, '*')
        window.refresh()
        sleep(0.05)


def main():
    curses.wrapper(pbar)


if __name__ == '__main__':
    main()
