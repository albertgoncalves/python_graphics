#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import random
import turtle


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
        boundary.pensize(1)
        boundary.color('white')
        boundary.speed(0)

        for side in range(4):
            boundary.forward(bounds_dist * 2)
            boundary.left(90)

        boundary.hideturtle()
        turtle.update()

    def create_player_object(coords, orientation, shape, size, color='white'):
        player_object = turtle.Turtle()
        player_object.color(color)
        player_object.shape(shape)
        player_object.penup()
        player_object.speed(0)
        player_object.setpos(*coords)
        player_object.setheading(orientation)
        player_object.shapesize(size, size)
        return player_object

    def listen_arrowkeys(player):

        def assign_movement(player, heading, key):
            turtle.onkeypress(set_heading(player, heading), key)
            turtle.onkeyrelease(speed_off, key)

        def set_heading(player, heading):
            return lambda: enable_movement(player, heading)

        def enable_movement(player, heading):
            player.setheading(heading)
            speed_on()

        def speed_on():
            global player_speed
            player_speed = 4

        def speed_off():
            global player_speed
            player_speed = 0

        turtle.listen()

        headings_to_keys = [ (  0, 'Right')
                           , (180, 'Left' )
                           , ( 90, 'Up'   )
                           , (270, 'Down' )
                           ]

        for heading, key in headings_to_keys:
            assign_movement(player, heading, key)


    def end_loop():
        global loop
        loop = False

    def check_bounds(player_object, bounds_dist):
        return ( (player_object.xcor() >  bounds_dist)
               | (player_object.xcor() < -bounds_dist)
               | (player_object.ycor() >  bounds_dist)
               | (player_object.ycor() < -bounds_dist)
               )

    def create_goal():
        return create_player_object( random_start(bounds_safe)
                                   , random.randint(0, 360)
                                   , 'square'
                                   , 2
                                   )

    global player_speed; player_speed = 0
    global loop        ; loop         = True
    bounds_dist = 275
    bounds_safe = int(bounds_dist * 0.65)
    n_goals     = 4
    goal_speed  = 3

    init_screen()
    draw_boundary(bounds_dist)
    player = create_player_object(random_start(bounds_safe), 90, 'triangle', 1)
    goals  = list(map(lambda _: create_goal(), range(n_goals)))

    while loop:
        player.forward(player_speed)
        listen_arrowkeys(player)

        for player_object in [player] + goals:
            if check_bounds(player_object, bounds_dist):
                player_object.right(180)

        for goal in goals:
            goal.forward(goal_speed)

            if distance(player, goal) < 10:
                goal.setpos(*random_start(bounds_safe))
                goal.right(random.randint(0, 360))

        turtle.update()


if __name__ == '__main__':
    main()
