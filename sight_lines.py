#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def flip_tuple(x, y):
    return y, x


def flip_x(x, y):
    return -x, y


def flip_y(x, y):
    return x, -y


def add_tuples(ab, cd):
    a, b = ab
    c, d = cd
    return a + c, b + d


def apply_tuple(f):
    return lambda xy: f(*xy)


def sight_dict():

    def apply_flip(f, xy):
        return list(map(apply_tuple(f), sights[f(*xy)]))

    sights = { (2, 2): [ (1, 1), (1, 2), (1, 3)
                       , (2, 1), (2, 2), (2, 3), (2, 4), (2, 5)
                       , (3, 1), (3, 2), (3, 3), (3, 4), (3, 5)
                       , (4, 2), (4, 3), (4, 4)
                       , (5, 2), (5, 3)
                       ]
             , (0, 2): [ (-2, 4), (-2, 5)
                       , (-1, 2), (-1, 3), (-1, 4), (-1, 5)
                       , ( 0, 1), ( 0, 2), ( 0, 3), ( 0, 4), ( 0, 5)
                       , ( 1, 2), ( 1, 3), ( 1, 4), ( 1, 5)
                       , ( 2, 4), ( 2, 5)
                       ]
             , (1, 2): [ (0, 1), (0, 2), (0, 3)
                       , (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)
                       , (2, 1), (2, 2), (2, 3), (2, 4), (2, 5)
                       , (3, 3), (3, 4)
                       , (4, 3), (4, 4)
                       ]
             }

    f_xys = [ (flip_tuple, ( 2,  0))
            , (flip_tuple, ( 2,  1))
            , (flip_y    , ( 2, -1))
            , (flip_y    , ( 2, -2))
            , (flip_y    , ( 1, -2))
            , (flip_y    , ( 0, -2))
            , (flip_x    , (-1, -2))
            , (flip_x    , (-2, -2))
            , (flip_x    , (-2, -1))
            , (flip_x    , (-2,  0))
            , (flip_y    , (-2,  1))
            , (flip_y    , (-2,  2))
            , (flip_x    , (-1,  2))
            ]

    for f, xy in f_xys:
        sights[xy] = apply_flip(f, xy)

    return sights


def main():
    sights = sight_dict()

    for key in list(sights.keys())[-1:]:
        print(key, list(map(lambda xy: add_tuples((10, 10), xy), sights[key])))

    print(len(sights.keys()))


if __name__ == '__main__':
    main()
