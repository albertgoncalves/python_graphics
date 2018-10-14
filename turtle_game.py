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


# def smudge(val):
#     return val + (val * (0.075 * (random.random() - 0.5)))


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

    def create_player_object(coords, shape, color='white'):
        player_object = turtle.Turtle()
        player_object.color(color)
        player_object.shape(shape)
        player_object.penup()
        player_object.speed(0)
        player_object.setpos(*coords)
        player_object.right(random.randint(0, 360))
        return player_object

    def listen_arrowkeys(player):
        turtle.listen()
        turtle.onkey( turn_left(player), 'Left' )
        turtle.onkey(turn_right(player), 'Right')
        turtle.onkey(    increase_speed, 'Up'   )
        turtle.onkey(    decrease_speed, 'Down' )

    def increase_speed():
        global player_speed
        if player_speed < 4:
            player_speed += 1

    def decrease_speed():
        global player_speed
        if player_speed > 1:
            player_speed -= 1

    def end_loop():
        global loop
        loop = False

    def check_bounds(player_object, bounds_dist):
        return ( (player_object.xcor() >  bounds_dist)
               | (player_object.xcor() < -bounds_dist)
               | (player_object.ycor() >  bounds_dist)
               | (player_object.ycor() < -bounds_dist)
               )

    global player_speed; player_speed = 1
    global loop ; loop  = True
    bounds_dist = 275

    init_screen()
    draw_boundary(bounds_dist)
    player = create_player_object(random_start(bounds_dist), 'triangle')
    goal   = create_player_object(random_start(bounds_dist), 'circle')

    while loop:
        listen_arrowkeys(player)

        player.forward(player_speed)
        goal.forward(4)

        if check_bounds(player, bounds_dist):
            player.right(180)

        if check_bounds(goal, bounds_dist):
            goal.right(180)

        if distance(player, goal) < 10:
            goal.setpos(*random_start(bounds_dist))
            goal.right(random.randint(0, 360))
            # loop = False

        turtle.update()


if __name__ == '__main__':
    main()
