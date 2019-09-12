import turtle  # really simple module to create games - creates 'turtles'
import random  # for the spawn and orientation of the goal
import math  # for the collide function

# setting up the main screen, the background color and the title
turtlegame = turtle.Screen()
turtlegame.bgcolor('black')
turtlegame.title("Snake_like_game")


class Border(turtle.Turtle):  # child class of the Turtle

    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.hideturtle()
        self.speed(0)
        self.color('white')  # making the borders white
        self.pensize(5)  # making the borders 5 pixels wide

    def draw_border(self):
        self.penup()  # penup so it doesnt start drawing immediately
        self.goto(-300, -300)
        self.pendown()
        self.goto(-300, 300)
        self.goto(300, 300)
        self.goto(300, -300)
        self.goto(-300, -300)


class Player(turtle.Turtle):

    def __init__(self):
        turtle.Turtle.__init__((self))
        self.penup()
        self.speed(0)
        self.shape('triangle')
        self.color('white')
        self.speed = 1

    def move(self):
        self.forward(self.speed)

        if self.xcor() > 285 or self.xcor() < - 285:
            self.left(90)
        if self.ycor() > 285 or self.ycor() < -285:
            self.left(90)

    def turnleft(self):
        self.left(45)

    def turnright(self):
        self.right(45)

    def increasespeed(self):
        self.speed += 1

    def decreasespeed(self):
        self.speed -= 1


# creating the goal of the game
class Goal(turtle.Turtle):

    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.color('yellow')
        self.shape('circle')
        self.speed = 2
        # so that it spawns at a random location with a random orientation for direction
        self.goto(random.randint(-250, 250), random.randint(-250, 250))
        self.setheading(random.randint(0, 360))

    # when you reach it with the player it would respawn
    def respawn(self):
        self.goto(random.randint(-250, 250), random.randint(-250, 250))
        self.setheading(random.randint(0, 360))

    # it moves the same way the player moves
    def move(self):
        self.forward(self.speed)

        if self.xcor() > 285 or self.xcor() < - 285:
            self.left(90)
        if self.ycor() > 285 or self.ycor() < -285:
            self.left(90)


# using pythagorean therom to measure the distance between the 2 objects
def isCollision(t1, t2):
    a = t1.xcor() - t2.xcor()
    b = t1.ycor() - t2.ycor()
    distance = math.sqrt((a ** 2) + (b ** 2))
    # and decide if they collide
    if distance < 20:
        return True
    else:
        return False


player = Player()
border = Border()
goal = Goal()

border.draw_border()

turtle.listen()
turtle.onkey(player.turnleft, 'Left')
turtle.onkey(player.turnright, 'Right')
turtle.onkey(player.increasespeed, 'Up')
turtle.onkey(player.decreasespeed, 'Down')

while True:
    player.move()
    goal.move()

    if isCollision(player, goal):
        goal.respawn()
