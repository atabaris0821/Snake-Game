from tkinter import *
import random
import time

class Snake(Tk):
    def __init__(self, *args, **kwargs):
        global highest_score
        Tk.__init__(self, *args, **kwargs)
        self.game_over_text = None
        self.initialSetup()
    with open("a.txt", "r") as f:
        highest_score = int(f.read())
        

    def initialSetup(self):
        global score, highest_score

        self.base = Canvas(self, width=1900, height=900, bg="lightgreen")  # Use 'bg' for background color
        self.base.pack(padx=10, pady=10)
        self.snake = self.base.create_rectangle(1, 1, 21, 21, fill="DodgerBlue2")
        self.score = 0
        
        self.scoreDisplay = Label(self, text="Score: {}\n Highest Score: {}".format(self.score, self.highest_score), font=('arial', 20, 'bold'))
        self.scoreDisplay.pack(anchor='n')

        # Add a restart button
        self.restartButton = Button(self, text="Restart Game", font=('arial', 20, 'bold'), command=self.restart)
        self.restartButton.pack(anchor='n')

        self.length = 3
        self.target = None
        self.gameStatus = 1
        self.x = 20
        self.y = 0
        self.bodycoords = [(0, 0)]
        self.bind('<Any-KeyPress>', self.linkKeys)

    def check_snake_coords(self):
        self.base.move(self.snake, self.x, self.y)
        i, j, ii, jj = self.base.coords(self.snake)
        if i <= 0 or j <= 0 or ii >= 1900 or jj >= 900:
            self.x = 0
            self.y = 0
            # Game over
            self.game_over_text = self.base.create_text(950, 450, text="GAME OVER", font=('arial', 70, 'bold'), fill='red')
            self.gameStatus = 0
    def move_snake(self):
        i, j, ii, jj = self.base.coords(self.snake)
        ii = (ii - ((ii - i) / 2))
        jj = (jj - ((jj - j) / 2))
        self.bodycoords.append((ii, jj))
        
        # Check if the snake collides with its own body
        if len(self.bodycoords) > self.length:
            self.base.delete('snakebody')
            del self.bodycoords[0]

        # Check for collisions with the rest of the body
        for segment in self.bodycoords[:-1]:
            if (ii, jj) == segment:
                self.x = 0
                self.y = 0
                # Game over
                self.game_over_text = self.base.create_text(950, 450, text="GAME OVER", font=('arial', 70, 'bold'), fill='red')
                self.gameStatus = 0

        self.base.create_line(tuple(self.bodycoords), tag='snakebody', width=20, fill="DodgerBlue2")
    def food(self):
        if self.target is None:
            a = random.randint(20, 1900)
            b = random.randint(20, 900)
            self.target = self.base.create_oval(a, b, a + 20, b + 20, fill='red', tag='food')

        if self.target:

            i, j, ii, jj = self.base.coords(self.target)

            if len(self.base.find_overlapping(i, j, ii, jj)) != 1:
                self.base.delete("food")
                self.target = None
                self.updateScore()
                self.length += 1
                
                

    def updateScore(self):
        self.score += 1
        if self.score >= self.highest_score:
            self.highest_score = self.score
            with open("a.txt", "w") as f:
                f.write(str(self.highest_score))
        self.scoreDisplay['text'] = "Score: {}\nhighest score:{}".format(self.score,self.highest_score)

    def linkKeys(self, event=None):
        pressedkey = event.keysym
        if pressedkey == 'Left':
            self.x = -20
            self.y = 0
        elif pressedkey == 'Up':
            self.x = 0
            self.y = -20
        elif pressedkey == 'Right':
            self.x = 20
            self.y = 0
        elif pressedkey == 'Down':
            self.x = 0
            self.y = 20
        else:
            pass

    def restart(self):
        # Reset the game state
        if self.game_over_text is not None:
            self.base.delete(self.game_over_text)
        self.base.delete("food")
        self.target = None
        self.gameStatus = 1
        self.x = 20
        self.y = 0
        self.bodycoords = [(0, 0)]
        self.score = 0
        self.scoreDisplay['text'] = "Score: {}\n highest score: {}".format(self.score, self.highest_score)
        self.length = 3
        self.base.delete("snakebody")
        self.base.coords(self.snake, 1, 1, 21, 21)

    def manage(self):
        if self.gameStatus == 0:
            return
        self.check_snake_coords()
        self.move_snake()
        self.food()

snakeobj = Snake(className="ProjectGurukul Snake Game")
with open("a.txt", "r") as f:
    highest_score = int(f.read())
while True:

    snakeobj.update()
    snakeobj.update_idletasks()
    snakeobj.manage()
    time.sleep(0.05)