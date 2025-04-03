import torch
import random
import numpy as np
import argparse
from collections import deque, namedtuple
from game import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot

parser = argparse.ArgumentParser()

#Argument 1 selects: rewards: -10 for lose, +10 for scoring (Original)
#Argument 2 selects: -10 for lose, -1 for moving away, +10 for scoring, +1 for moving towards. (Frequent rewards)
#Argument 3 selects: -20 for lose, -2 for moving away, +10 for scoring, +1 for moving towards. (Frequent rewards, Increase penalty)
#Argument 4 selects: -(10+score * 3) for lose, -1 for moving away, +(10+score * 3) for scoring, +1 for moving towards. (Frequent rewards, Adaptive reward)
#Argument 5 selects: -(10+score * 3) for lose, -2 for moving away, +(10+score * 3) for scoring, +1 for moving towards. (Frequent rewards, Increase penalty, Adaptive reward)
parser.add_argument('x',type=float)
parser.add_argument('y',type=int)
parser.add_argument('--expected','-e',type=float)
args = parser.parse_args()

REWARD_CONFIG = args.x
STATE_CONFIG = args.y

print(REWARD_CONFIG)
print(STATE_CONFIG)

if args.expected is not None and args.expected != REWARD_CONFIG:
    print(f"Expected {args.expected} but got {REWARD_CONFIG}")

input_size = -1

#Initialise empty array
#Added inputs

Point = namedtuple('Point', 'x, y')
BLOCK_SIZE = 20
add_inputs = []
grid_size = STATE_CONFIG*2 + 1
for i in range((STATE_CONFIG*2 + 1)**2):
    j = i%grid_size
    k = i//grid_size
    temp_point = Point(-20 + 20*j,-20 + 20*k)
    add_inputs.append(temp_point)
print(add_inputs)

input_size = 11 + (STATE_CONFIG*2 + 1)**2
print("Input Size:" + str(input_size))


print("Reward Config: " + str(REWARD_CONFIG))
print("State Config: " + str(STATE_CONFIG))
#Argument 1 selects: rewards: -10 for lose, +10 for scoring (Original)

    #SnakeGameAI(640,480,5)
    #print(SnakeGameAI.reward_type)

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001



class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(input_size, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        point_x = point_d + point_u + head

        point_l2 = Point(head.x - 40, head.y)
        point_r2 = Point(head.x + 40, head.y)
        point_u2 = Point(head.x, head.y - 40)
        point_d2 = Point(head.x, head.y + 40)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN


        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]

        # Append more inputs in state
        for i in add_inputs:
            i = Point(head.x +i.x,head.y+i.y)
            state.append(game.is_collision(i))
        # print(state)
        # print(len(state))
            
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    game.reward_type = REWARD_CONFIG
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
            #print(reward)

if __name__ == '__main__':
    train()