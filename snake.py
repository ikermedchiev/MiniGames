import tkinter as tk
from collections import deque as dq
import random


class Cell:
    def __init__(self, x, y, square):
        self.x = x
        self.y = y
        self.square = square

    def __iter__(self):
        yield self.x
        yield self.y


class Snake:
    def __init__(self, parent):
        self.parent = parent
        self.WIDTH = 600
        self.HEIGHT = 600
        self.CELL = 50
        self.max_speed_score = 500  # stop increasing speed at this score
        self.speed_factor = 40  # increase speed every x points
        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack()
        self.parent.bind('<Control-n>', self.draw_board)
        self.parent.bind('<Left>', self.tick)
        self.parent.bind('<Right>', self.tick)
        self.parent.bind('<Up>', self.tick)
        self.parent.bind('<Down>', self.tick)
        self.draw_board()

    def draw_board(self, event=None):
        self.direction = 'Right'
        self.tickrate = 1000
        self.score = 1
        self.canvas.delete(tk.ALL)
        self.empty = [(x, y) for x in range(0, self.WIDTH, self.CELL)
                      for y in range(0, self.HEIGHT, self.CELL)]
        x, y = self.empty.pop(len(self.empty) // 2 + int(0.5 * len(self.empty) ** 0.5))
        # the head is 0 and the tail is -1
        self.snake = dq([Cell(x, y, self.canvas.create_rectangle(x,
                                                                 y,
                                                                 x + self.CELL,
                                                                 y + self.CELL,
                                                                 fill='blue'))])
        self.create_food()
        self.ticking = self.parent.after(self.tickrate, self.tick)
        self.running = True

    def create_food(self):
        try:
            x, y = self.empty.pop(random.randrange(len(self.empty)))
        except ValueError:
            self.end(f'You win!\nScore: {self.score}.')
        else:
            self.food = Cell(x, y, self.canvas.create_rectangle(x, y, x + self.CELL, y + self.CELL, fill='red'))
            if self.score <= self.max_speed_score:
                self.tickrate = 1000 // (self.score // self.speed_factor + 1)

    def move(self, direction):
        head = self.snake[0]
        tail = self.snake[-1]
        x, y = head
        if direction == 'Left':
            target = x - self.CELL, y
        elif direction == 'Right':
            target = x + self.CELL, y
        elif direction == 'Up':
            target = x, y - self.CELL
        else:
            target = x, y + self.CELL
        # collision detection etc.
        if target == tuple(self.food):
            self.snake.appendleft(self.food)
            self.score += 1
            self.recolor()
            self.create_food()
            return
        if target in self.empty or target == tuple(tail):
            self.empty.append(tuple(tail))
            self.empty.remove(target)
            tail.x, tail.y = target
            self.canvas.coords(tail.square, *target, *(a + self.CELL for a in target))
            self.snake.appendleft(self.snake.pop())
            self.recolor()
            return
        self.end(f'You lose.\nScore: {self.score}.')

    def recolor(self):
        self.canvas.itemconfig(self.snake[0].square, fill='blue')
        if len(self.snake) > 1:
            self.canvas.itemconfig(self.snake[1].square, fill='black')

    def tick(self, event=None):
        if event:
            direction = event.keysym
            if {direction, self.direction} in ({'Left', 'Right'},
                                               {'Up', 'Down'}):
                return
            self.direction = direction
            self.parent.after_cancel(self.ticking)
        if self.running:
            self.move(self.direction)
            self.ticking = self.parent.after(self.tickrate, self.tick)

    def end(self, text):
        self.parent.after_cancel(self.ticking)
        self.running = False
        self.canvas.create_text(self.WIDTH // 2,
                                self.HEIGHT // 2,
                                text=text,
                                font=('Times', self.HEIGHT // 10),
                                fill='orange')


root = tk.Tk()
snake = Snake(root)
root.mainloop()
