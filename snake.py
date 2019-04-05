import keyboard 
import pygame as pg
import time
import random as r
import numpy as np
import json

class SnakeGame:

    def __init__(self, dim, square_interval):
        self.P1_COLOR = (255,255,255)
        self.FOOD_COLOR = (150,150,150)   
        self.BORDER_COLOR = (75,75,75)

        self.x = dim
        self.y = dim
        
        self.snake_dimensions = square_interval//2
        self.i = square_interval
        self.interval = dim//square_interval

        self._reset_game()
        
    def _get_random_location(self):
        availabe = []

        # Get a list of all possible locations that are not occupied or on an edge
        for row in range(self.interval):
            for col in range(self.interval):
                if self.grid[row][col] == 0 and (1 < row < self.interval - 2) and (1 < col < self.interval - 2):
                    availabe.append((col, row))
        return r.choice(availabe)

    def _reset_board(self):

        self.grid = []
        
        # Reset grid and draw border on grid
        for row in range(self.interval):
            a = []
            for col in range(self.interval):
                if row == 0 or col == 0 or row == self.interval-1 or col == self.interval-1:
                    a.append(3)
                else:
                    a.append(0)
            self.grid.append(a)

    def _reset_game(self):

        # Reset the game and init params
        self._reset_board()
        self.game_over = False
        self.snake_length = 1
        self.P1_POS = [(self.interval//2, self.interval//2)]
        self.food_position = self._get_random_location()
        self.P1_DIR = r.randint(0, 3)

    def get_game_state(self):
    
        """
        0 - Game is over
        1 - Game is in progress
        2 - Player won
        """
    
        if self.game_over:
            return 0
        else:
            a = False
            for row in range(self.interval):
                for col in range(self.interval):
                    if self.grid[row][col] == 0:
                        a = True
            return int(a) + 1

    def get_input_data(self, pos):
        """
        Input is a vector with dimension (13,)
        """ 
        x, y = pos
        fx, fy = self.food_position
        output = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        adjacent_data = self.get_adjacent_data(pos)

        # Get Adjacent Wall
        output[0] = float(adjacent_data[0] == 3)
        output[1] = float(adjacent_data[1] == 3)
        output[2] = float(adjacent_data[2] == 3)
        output[3] = float(adjacent_data[3] == 3)

        # Get Adjacent Body
        output[4] = float(adjacent_data[0] == 1)
        output[5] = float(adjacent_data[1] == 1)
        output[6] = float(adjacent_data[2] == 1)
        output[7] = float(adjacent_data[3] == 1)

        # Get Food Direction
        output[8] = float(fx == x and fy < y) # Food Above
        output[9] = float(fx == x and fy > y) # Food Below
        output[10] = float(fy == y and fx < x) # Food Left
        output[11] = float(fy == y and fx > x) # Food Right

        # Current movement direction
        output[12] = (self.P1_DIR+1)/4

        return output

    def get_adjacent_data(self, pos):
       
        y, x = pos

        down, up, right, left = None, None, None, None

        if self.check_position((x, y+1)):
            down = self.grid[x][y+1]
        
        if self.check_position((x, y-1)):
            up = self.grid[x][y-1]
        
        if self.check_position((x+1, y)):
            right = self.grid[x+1][y]
        
        if self.check_position((x-1, y)):
            left = self.grid[x-1][y]
        
        a = [up, down, left, right]
        return a

    def check_position(self, pos):
        x, y = pos
        return not (x < 0 or y < 0 or x > self.interval-1 or y > self.interval-1)
    
    def run_game(self, delay, games=None):

        screen = pg.display.set_mode((self.x, self.y))
        training_labels = []

        game = 0
        k = 10

        if games:
            k = games

        while game < k:

            self._reset_game()

            while self.get_game_state():

                screen.fill((0,0,0))
                self._reset_board()

                # Draw Border
                pg.draw.rect(screen, self.BORDER_COLOR, (0, 0, self.x, self.snake_dimensions*2))
                pg.draw.rect(screen, self.BORDER_COLOR, (0, 0, self.snake_dimensions*2, self.y))
                pg.draw.rect(screen, self.BORDER_COLOR, (0, self.y - self.snake_dimensions*2, self.x, self.snake_dimensions*2))
                pg.draw.rect(screen, self.BORDER_COLOR, (self.x - self.snake_dimensions*2, 0, self.snake_dimensions*2, self.y))


                for position in self.P1_POS:
                    sx = position[0] 
                    sy = position[1] 

                    # Check If Snake Ate Itself
                    if self.grid[sy][sx] == 1 or sx <= 0 or sy <= 0 or sx >= self.interval-1 or sy >= self.interval-1:
                        self.game_over = True
                        break
                        
                    # Draw Snake
                    pg.draw.rect(screen, self.P1_COLOR, (sx*self.i, sy*self.i, self.snake_dimensions*2, self.snake_dimensions*2))                    
                    self.grid[sy][sx] = 1
                
                if self.get_game_state:

                    # Draw Food
                    fx = self.food_position[0]
                    fy = self.food_position[1]            
                    pg.draw.rect(screen, self.FOOD_COLOR, (fx*self.i, fy*self.i, self.snake_dimensions*2, self.snake_dimensions*2))           
                    self.grid[fx][fy] = 2
                
                    pg.display.update()
                            
                    # Check If Snake Ate Food
                    if self.P1_POS[0] == self.food_position:
                        self.food_position = self._get_random_location()    
                        self.snake_length += 1

                    # Get Keyboard Input
                    if keyboard.is_pressed('w'):
                        self.P1_DIR = 0
                    elif keyboard.is_pressed('a'):
                        self.P1_DIR = 2
                    elif keyboard.is_pressed('s'):
                        self.P1_DIR = 1
                    elif keyboard.is_pressed('d'):
                        self.P1_DIR = 3

                    if keyboard.is_pressed('/'):
                        quit(0)
                    
                    # Update Current Position Based on Movement State
                    pos = None
                    curr_position = self.P1_POS[0]
                    curr_x = curr_position[0]
                    curr_y = curr_position[1]
                    if self.P1_DIR == 0:
                        curr_y -= 1
                    elif self.P1_DIR == 1:
                        curr_y += 1
                    elif self.P1_DIR == 2:
                        curr_x -= 1
                    elif self.P1_DIR == 3:
                        curr_x += 1
                    pos = (curr_x % (self.interval), curr_y % (self.interval))    
                    
                    # Pop end of snake to maintain size
                    self.P1_POS.insert(0, pos)
                    if len(self.P1_POS) > self.snake_length:
                        self.P1_POS.pop()

                    time.sleep(delay)
            
            print("GAME OVER.", "Score:", self.snake_length) 
            if games:
                game += 1

def main():
    snake = SnakeGame(500, 20)
    snake.run_game(0.08)

if __name__ == "__main__":
    main()
