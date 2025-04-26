# Study of improvement attempts made to "snake-ai-pytorch" repository

This repository documents several attempts at improving original repo in terms of score of AI.

Original repo is a Python Reinforcement Learning Tutorial series that teaches an AI to play Snake.

You may find the Youtube video detailing this here: [Playlist](https://www.youtube.com/playlist?list=PLqnslRFeH2UrDh7vUmJ60YrmWd64mTTKV)

# Contents

- Adaptive Reward
- Increase inputs
- Layer Shenanigans

# Adaptive Reward

## Introduction
Made certain alterations to the reward system of original repo.

There are 4 parameters currently that are used to alter the reward system. Reward #1-4 is a combination/change of these 4 parameters. 
Below explains the 4 parameters and what they do.
###Parameter#1: 
'''
self.reward_loss_1
'''
Reward hitting wall/self
### Parameter#2:
'''
self.reward_loss_2
'''
Reward moving away from food

## Reward#1 (-10 for lose, +10 for scoring (Original))
First reward is the original reward system, serves as a baseline.

![AdaptiveReward-1](https://github.com/user-attachments/assets/b00f7c67-90b5-4212-ae78-a0571b93b95e)

## Reward#2 (-10 for lose, +10 for scoring (Original))
# Increase inputs

# Layer Shenanigans
