#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import random
import turtle


def turn_left(player):
    return lambda: player.left(30)


def turn_right(player):
    return lambda: player.right(30)


def distance(turtle_a, turtle_b):
    x = turtle_a.xcor() - turtle_b.xcor()
    y = turtle_a.ycor() - turtle_b.ycor()
    return math.sqrt((x ** 2) + (y ** 2))


def random_loc(bounds_dist):
    return random.randint(-bounds_dist, bounds_dist)


def random_start(bounds_dist):
    return random_loc(bounds_dist), random_loc(bounds_dist)


def main():

    def init_screen():
        turtle.tracer(0, 0)

        wn = turtle.Screen()
        wn.bgcolor('black')

        wn.listen()
        wn.onkeypress(end_loop, 'q')

    def draw_boundary(bounds_dist):
        boundary = turtle.Turtle()
        boundary.penup()
        boundary.setpos(-bounds_dist, -bounds_dist)
        boundary.pendown()
        boundary.pensize(3)
        boundary.color('white')
        boundary.speed(0)

        for side in range(4):
            boundary.forward(bounds_dist * 2)
            boundary.left(90)

        boundary.hideturtle()
        turtle.update()

    def create_player_object(coords, color, shape):
        player_object = turtle.Turtle()
        player_object.color(color)
        player_object.shape(shape)
        player_object.penup()
        player_object.speed(0)
        player_object.setpos(*coords)
        return player_object

    def listen_arrowkeys(player):
        turtle.listen()
        turtle.onkey( turn_left(player), 'Left' )
        turtle.onkey(turn_right(player), 'Right')
        turtle.onkey(    increase_speed, 'Up'   )
        turtle.onkey(    decrease_speed, 'Down' )

    def increase_speed():
        global speed
        if speed < 4:
            speed += 1

    def decrease_speed():
        global speed
        if speed > 1:
            speed -= 1

    def end_loop():
        global loop
        loop = False

    global speed; speed = 1
    global loop ; loop  = True
    bounds_dist = 275

    init_screen()
    draw_boundary(bounds_dist)
    player = create_player_object(random_start(bounds_dist), 'white', 'square')
    goal   = create_player_object(random_start(bounds_dist), 'white', 'circle')

    listen_arrowkeys(player)

    while loop:
        player.forward(speed)

        if (player.xcor() > bounds_dist) | (player.xcor() < -bounds_dist):
            player.right(180)

        if (player.ycor() > bounds_dist) | (player.ycor() < -bounds_dist):
            player.right(180)

        if distance(player, goal) < 10:
            loop = False

        turtle.update()


if __name__ == '__main__':
    main()
