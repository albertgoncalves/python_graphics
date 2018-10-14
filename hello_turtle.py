#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import turtle


def main():
    turtle.color('red', 'yellow')
    turtle.begin_fill()

    while True:
        turtle.forward(200)
        turtle.left(170)
        if abs(turtle.pos()) < 1:
            break

    turtle.end_fill()
    turtle.done()


if __name__ == '__main__':
    main()
