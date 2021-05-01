import tkinter as tk
import json
import random as r

f = open('config.json', 'r')
config = json.load(f)

# Main
class Game:
    def __init__(self):
        # Init
        self.direction = 'Stop'
        self.isAlive = True
        self.cols = config['cols']
        self.rows = config['rows']
        self.length = config['length']
        self.tick = config['tick']
        self.snake = [[int(self.cols / 2), int(self.rows / 2)]] * self.length
        self.w = config['cols'] * config['size'] + config['cols'] - 1
        self.h = config['rows'] * config['size'] + config['rows'] - 1
        self.htext = 30
        self.root = tk.Tk()
        self.root.title(config['title'])
        self.root.geometry('{}x{}{}'.format(self.w, self.h + self.htext, '+500+300'))
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width = self.w, height = self.h, bg = config['color']['bg'], bd = 2)
        self.canvas.pack(side = 'top')
        self.pointText = tk.StringVar()
        self.points = tk.Label(self.root, width = self.w, height = self.htext, bg = config['color']['bg'], textvariable = self.pointText)
        self.points.pack(side = 'bottom')
        self.grid()

        # Start
        self.root.bind('<Key>', self.setDirection)
        self.food = self.spawnFood()
        self.move()
        self.root.mainloop()

    def grid(self):
        for i in range(1, config['cols']):
            p = i * config['size'] + i
            self.canvas.create_line(p, 0, p, self.h, fill = config['color']['grid'])

        for i in range(1, config['rows']):
            p = i * config['size'] + i
            self.canvas.create_line(0, p, self.w, p, fill = config['color']['grid'])

    def fill(self, x, y, color = config['color']['bg']):
        x1 = x * config['size'] + x + 1
        x2 = x1 + config['size']
        y1 = y * config['size'] + y + 1
        y2 = y1 + config['size']
        self.canvas.create_polygon(x1, y1, x2, y1, x2, y2, x1, y2, fill = color)

    def setDirection(self, event):
        if event.keysym == 'Up' or event.keysym == 'Down' or event.keysym == 'Right' or event.keysym == 'Left':
            isOpposite =  event.keysym == 'Up' and self.direction == 'Down'
            isOpposite = isOpposite or event.keysym == 'Down' and self.direction == 'Up'
            isOpposite = isOpposite or event.keysym == 'Right' and self.direction == 'Left'
            isOpposite = isOpposite or event.keysym == 'Left' and self.direction == 'Right'
            if not isOpposite:
                self.direction = event.keysym

    def shift(self):
        tail = self.snake.pop()
        self.snake.insert(0, self.snake[0])
        if tail not in self.snake:
            self.fill(tail[0], tail[1])

    def move(self):
        self.shift()
        if self.direction == 'Up':
            self.snake[0] = [self.snake[0][0], self.snake[0][1] - 1]
        elif self.direction == 'Down':
            self.snake[0] = [self.snake[0][0], self.snake[0][1] + 1]
        elif self.direction == 'Right':
            self.snake[0] = [self.snake[0][0] + 1, self.snake[0][1]]
        elif self.direction == 'Left':
            self.snake[0] = [self.snake[0][0] - 1, self.snake[0][1]]

        self.checkCollision(self.snake[0])
        self.checkFood(self.snake[0])

        if self.isAlive:
            self.draw()
            self.pointText.set('Point: {}'.format(self.length - 4))
            self.root.after(int(self.tick * 1000), self.move)

    def gameover(self):
        self.drawAll(config['color']['dead'])
        self.pointText.set('GAME OVER! Point: {}'.format(self.length - 4))

    def spawnFood(self):
        pos = [r.randint(0, self.cols - 1), r.randint(0, self.rows - 1)]
        while pos in self.snake:
            pos = [r.randint(0, self.cols - 1), r.randint(0, self.rows - 1)]
        self.fill(pos[0], pos[1], config['color']['food'])
        return pos

    def checkCollision(self, head):
        isOut = head[0] < 0 or head[0] >= self.cols or head[1] < 0 or head[1] >= self.rows
        isTwist = head in self.snake[1:]
        if (isOut or isTwist) and (self.direction != 'Stop'):
            self.isAlive = False
            self.direction = 'Stop'
            self.gameover()

    def checkFood(self, head):
        if head == self.food:
            self.snake.append(self.snake[-1])
            self.length += 1
            self.food = self.spawnFood()

    def drawAll(self, color = config['color']['snake']):
        for i in self.snake:
            self.fill(i[0], i[1], color)

    def draw(self, color = config['color']['snake']):
        self.fill(self.snake[0][0], self.snake[0][1], color)

game = Game()
