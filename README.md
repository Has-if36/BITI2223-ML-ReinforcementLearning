## University Assignment 2 under Machine Learning Subject (BITI2223)

Upon creating this repo and uploading the code, it has been quite some time since I coded this. During that time, I was relatively new to python. I may forgot how this works. Hehe..
  
For this assignment, I was tasked to implement a reinforcement learning. I made a simple game that AI can learn. So, I made a game similar to The Dinosaur Game (basically just knockoff version of that game). This time, the golden block is the Dino while the red block is the obstacle
  
## Environment
### Agent
The agent is the golden block / Dino itself
  
### Observation
The dino is able to see types of obstacle as well as the distance between the Dino and the Obstacle (when it gets near)
  
### Action
The Dino is able to perform 3 action, which is Jump, Duck or Do Nothing. 
  
### Reward
Everytime the Dino is able to pass the obstacle, it will get the reward.
  
### Punishment
Everytime it gets hit on obstacle, it will receive punishment.
  
## Results
<p align="center">
  <img width="508" height="400" src="https://user-images.githubusercontent.com/55189926/158974115-337b1f66-3b86-483e-beff-62b862237614.png">
  <img width="471" height="400" src="https://user-images.githubusercontent.com/55189926/159007007-e7848715-8773-4f75-852b-679bdc4b8590.png">
  <br>
  Result
  <br>
</p>

From here we can see the AI barely learn and getting improve. Since the game speed gets faster as the Dino gets higher score, this may effect the decision of the AI to improve.  
Secondly, the observation for the distance between the Dino and the Obstacle (when it gets near) might also gave the AI much larger decision, where it gets to decide at which distance to take the action. This can also slow down the process for the AI to learn.  
Furthermore, having to get higher speed as it gets higher score, this can also give a disrupt to the AI, where it was actualy did the right decision, but the game was to fast for the Dino to react. This can affect the learning process and cause the AI learning process to fall.

