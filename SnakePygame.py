import random
import numpy as np
import pygame
import pickle
import time
class Color:
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (50, 150, 255)
        self.green = (200, 255, 0)
class VisualSnake:
    def __init__(self):
        self.show_episode = True
        self.episode = None
        self.scale = 2
        self.game_width = int(600 * self.scale)
        self.game_height = int(400 * self.scale)
        self.padding = int(30 * self.scale)
        self.screen_width = self.game_width
        self.screen_height = self.game_height + self.padding
        self.snake_size = int(10 * self.scale)
        self.food_size = int(10 * self.scale)
        self.snake_speed = 20
        self.snake_coords = []
        self.snake_length = 1
        self.dir = "right"
        self.board = np.zeros((self.game_height // self.snake_size, self.game_width // self.snake_size))
        self.game_close = False
        self.x1 = self.game_width / 2
        self.y1 = self.game_height / 2 + self.padding
        self.r1, self.c1 = self.coords_to_index(self.x1, self.y1)
        self.board[self.r1][self.c1] = 1
        self.c_change = 1
        self.r_change = 0
        self.food_r, self.food_c = self.generate_food()
        self.board[self.food_r][self.food_c] = 2
        self.survived = 0
        pygame.init()
        self.color = Color()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height)) 
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("bahnschrift", int(18 * self.scale))
        self.last_dir = None
        self.step()
    def print_score(self, score):
        value = self.font.render(f"Score: {score}", True, self.color.white)
        self.screen.blit(value, [500 * self.scale, 10])
    def print_episode(self):
        if self.show_episode:
            value = self.font.render(f"Episode: {self.episode}", True, self.color.white)
            self.screen.blit(value, [10, 10])
    def draw_snake(self):
        for i in range(len(self.snake_coords) - 1, -1, -1):
            r, c = self.snake_coords[i]
            x, y = self.index_to_coords(r, c)
            if i == len(self.snake_coords) - 1:
                pygame.draw.rect(self.screen, self.color.blue, [x, y, self.snake_size, self.snake_size])  # Face for the snake
            else:
                pygame.draw.rect(self.screen, self.color.green, [x, y, self.snake_size, self.snake_size])
    def game_end_message(self):
        mesg = self.font.render("Game over!", True, self.color.red)
        self.screen.blit(mesg, [2 * self.game_width / 5, 2 * self.game_height / 5 + self.padding])
    def is_unsafe(self, r, c):
        if self.valid_index(r, c):
          if self.board[r][c] == 1:
              return 1
          return 0
        else:
          return 1
    def get_state(self):
        head_r, head_c = self.snake_coords[-1]
        state = []
        state.append(int(self.dir == "left"))
        state.append(int(self.dir == "right"))
        state.append(int(self.dir == "up"))
        state.append(int(self.dir == "down"))
        state.append(int(self.food_r < head_r))
        state.append(int(self.food_r > head_r))
        state.append(int(self.food_c < head_c))
        state.append(int(self.food_c > head_c))
        state.append(self.is_unsafe(head_r + 1, head_c))
        state.append(self.is_unsafe(head_r - 1, head_c))
        state.append(self.is_unsafe(head_r, head_c + 1))
        state.append(self.is_unsafe(head_r, head_c - 1))
        return tuple(state)
    def valid_index(self, r, c):
        return 0 <= r < len(self.board) and 0 <= c < len(self.board[0])
    def index_to_coords(self, r, c):
        x = c * self.snake_size
        y = r * self.snake_size + self.padding
        return (x, y)
    def coords_to_index(self, x, y):
        r = int((y - self.padding) // self.snake_size)
        c = int(x // self.snake_size)
        return (r, c)
    def generate_food(self):
        food_c = int(round(random.randrange(0, self.game_width - self.food_size) / self.food_size))
        food_r = int(round(random.randrange(0, self.game_height - self.food_size) / self.food_size))
        if self.board[food_r][food_c] != 0:
            food_r, food_c = self.generate_food()
        return food_r, food_c
    def game_over(self):
        return self.game_close
    def step(self, action="None"):
        if action == "None":
            action = random.choice(["left", "right", "up", "down"])
        else:
            action = ["left", "right", "up", "down"][action]
        for event in pygame.event.get():
            pass
        self.last_dir = self.dir
        if action == "left" and (self.dir != "right" or self.snake_length == 1):
            self.c_change = -1
            self.r_change = 0
            self.dir = "left"
        elif action == "right" and (self.dir != "left" or self.snake_length == 1):
            self.c_change = 1
            self.r_change = 0
            self.dir = "right"
        elif action == "up" and (self.dir != "down" or self.snake_length == 1):
            self.r_change = -1
            self.c_change = 0
            self.dir = "up"
        elif action == "down" and (self.dir != "up" or self.snake_length == 1):
            self.r_change = 1
            self.c_change = 0
            self.dir = "down"
        if self.c1 >= self.game_width // self.snake_size or self.c1 < 0 or self.r1 >= self.game_height // self.snake_size or self.r1 < 0:
            self.game_close = True
        self.c1 += self.c_change
        self.r1 += self.r_change
        self.screen.fill(self.color.black)
        pygame.draw.rect(self.screen, (255, 255, 255), (0, self.padding, self.game_width, self.game_height), 1)
        food_x, food_y = self.index_to_coords(self.food_r, self.food_c)
        pygame.draw.rect(self.screen, self.color.red, [food_x, food_y, self.food_size, self.food_size])
        self.snake_coords.append((self.r1, self.c1))
        if self.valid_index(self.r1, self.c1):
            self.board[self.r1][self.c1] = 1
        if len(self.snake_coords) > self.snake_length:
            rd, cd = self.snake_coords[0]
            del self.snake_coords[0]
            if self.valid_index(rd, cd):
                self.board[rd][cd] = 0
        for r, c in self.snake_coords[:-1]:
            if r == self.r1 and c == self.c1:
                self.game_close = True
        self.draw_snake()
        self.print_score(self.snake_length - 1)
        self.print_episode()
        pygame.display.update()
        if self.c1 == self.food_c and self.r1 == self.food_r:
            self.food_r, self.food_c = self.generate_food()
            self.board[self.food_r][self.food_c] = 2
            self.snake_length += 1
        self.survived += 1
    def run_game(self, episode):
        self.show_episode = True
        self.episode = episode
        self.print_episode()
        pygame.display.update()
        filename = f"Q_table_results/{episode}.pickle"
        with open(filename, 'rb') as file:
            table = pickle.load(file)
        time.sleep(5)
        current_length = 2
        steps_unchanged = 0
        while not self.game_over():
            if self.snake_length != current_length:
                steps_unchanged = 0
                current_length = self.snake_length
            else:
                steps_unchanged += 1
            state = self.get_state()
            action = np.argmax(table[state])
            if steps_unchanged == 1000:
                break
            self.step(action)
            self.clock.tick(self.snake_speed)
        if self.game_over() == True:
            self.screen.fill(self.color.black)
            pygame.draw.rect(self.screen, (255, 255, 255), (0, self.padding, self.game_width, self.game_height), 1)
            self.game_end_message()
            self.print_episode()
            self.print_score(self.snake_length - 1)
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
        return self.snake_length
def main():
    try:
        episode = 100000
        visual_snake = VisualSnake()
        visual_snake.run_game(episode)
    except KeyboardInterrupt:
        print("!!!Done Already!!!")
if __name__ == "__main__":
    main()