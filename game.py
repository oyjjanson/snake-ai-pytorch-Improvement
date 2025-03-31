import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

sfont = pygame.font.Font('arial.ttf', 12)
head_text = sfont.render("Head",1,(100,100,255), (255,255,255))
head_past_text = sfont.render("Past",1,(100,100,255), (255,255,255))

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 40

class SnakeGameAI:
    def __init__(self, w=640, h=480, reward_type=0):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
        self.reward_type = reward_type
        self.reward = 0
        self.reward_loss_1 = -1
        self.reward_loss_2 = -1
        self.reward_gain_1 = -1
        self.reward_gain_2 = -1
        self.head_past = Point(-1, -1)
        #print("Reward Type: " + str(self.reward_type))

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0


    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()


    def play_step(self, action):
        
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)

        ########################## ADJUSTED AREA ##########################

        # 3. check if game over
        self.reward = 0
        # 3a. Different reward systems #1-5
        if self.reward_type == 1:
            self.reward_loss_1 = -10
            self.reward_loss_2 = 0
            self.reward_gain_1 = 10
            self.reward_gain_2 = 0
        if self.reward_type == 2:
            self.reward_loss_1 = -10
            self.reward_loss_2 = -1
            self.reward_gain_1 = 10
            self.reward_gain_2 = 1
        if self.reward_type == 3:
            self.reward_loss_1 = -20
            self.reward_loss_2 = -2
            self.reward_gain_1 = 10
            self.reward_gain_2 = 1
        if self.reward_type == 4:
            self.reward_loss_1 = -(10 + self.score * 3)
            self.reward_loss_2 = -1
            self.reward_gain_1 = 10 + self.score * 3
            self.reward_gain_2 = 1
        if self.reward_type == 5:
            self.reward_loss_1 = -(10 + self.score * 3)
            self.reward_loss_2 = -1
            self.reward_gain_1 = 10
            self.reward_gain_2 = 1

        food_v = pygame.Vector2(self.food)
        head_v = pygame.Vector2(self.head)
        past_v = pygame.Vector2(self.head_past)

        if food_v.distance_to(head_v) < food_v.distance_to(past_v):
            self.reward = self.reward_gain_1
        if food_v.distance_to(head_v) > food_v.distance_to(past_v):       
            self.reward = self.reward_loss_2

        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            self.reward = self.reward_loss_1
            return self.reward, game_over, self.score

        # 3b. Increased scoring based on moving towards or away from point



        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self.reward = self.reward_gain_1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        #print(self.test_arg)
        return self.reward, game_over, self.score

        ########################## ADJUSTED AREA ##########################

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False


    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(head_past_text, [self.head_past.x, self.head_past.y])
        self.display.blit(head_text, [self.head.x, self.head.y])
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir
        self.head_past = self.head

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
