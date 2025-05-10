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
### Parameters: 
```
Parameter#1: self.reward_loss_1 #Reward colliding with wall/self
Parameter#2: self.reward_loss_2 #Reward moving away from food
Parameter#3: self.reward_gain_1 #Reward after colliding with food
Parameter#4: self.reward_gain_2 #Reward moving toward food
```

## Reward#1 (-10 for lose, +10 for scoring (Original))
self.reward_loss_1 = -10<br>
self.reward_loss_2 = 0<br>
self.reward_gain_1 = +10<br>
self.reward_gain_2 = 0<br>
First reward is the original reward system, serves as a baseline.

![AdaptiveReward-1](https://github.com/user-attachments/assets/b00f7c67-90b5-4212-ae78-a0571b93b95e)

## Reward#2
self.reward_loss_1 = -10
<br>self.reward_loss_2 = -1
<br>self.reward_gain_1 = +10
<br>self.reward_gain_2 = +1
<br>Gives feedback per movement based on moving toward or away from food.

![AdaptiveReward-2](https://github.com/user-attachments/assets/deea8e44-52c5-4fb2-969a-eec015c75ea7)

## Reward#3
self.reward_loss_1 = -20
<br>self.reward_loss_2 = -2
<br>self.reward_gain_1 = +10
<br>self.reward_gain_2 = +1

![AdaptiveReward-3](https://github.com/user-attachments/assets/55233b08-3bb2-46f4-9f41-371a8d2160ea)

## Reward#4
self.reward_loss_1 = -(10 + self.score * 3)
<br>self.reward_loss_2 = -1
<br>self.reward_gain_1 = 10 + self.score * 3
<br>self.reward_gain_2 = +1

![AdaptiveReward-4](https://github.com/user-attachments/assets/a3180301-2f5a-4a1b-a6a2-1183965ad018)

## Reward#5
self.reward_loss_1 = -(10 + self.score * 3)
<br>self.reward_loss_2 = -1
<br>self.reward_gain_1 = +10
<br>self.reward_gain_2 = +1

![AdaptiveReward-5](https://github.com/user-attachments/assets/1d9ccaed-ba2a-4d7f-b6d5-a094177b3d68)

# Increase inputs

<br>Layer 1 inputs were increased by a variable^2. This represents the square grid around the snake head.
<br>Increasing layer inputs have shown to decrease overall score of agent. 
<br>
# Layer Shenanigans
