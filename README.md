# simple-maze-solver-program
This semester, I had a little AI &amp; Soft Computing project where we were taught a bunch of uninformed and informed algorithms. This is a simple project implementing exactly that. 

This little snippet of code is just over 400 lines and is a humble program that I wrote as a practice to the search algorithms we were taught during our lectures. 
This has 3 informed search algorithms implemented, and 3 uninformed, and also has a simple AI agent deciding which direction to go depending upon its path calculations.  
Uninformed Search: 
1. BFS
2. DFS
3. Iterative Deepening DFS

Informed Search:
1. Hill Climbing
2. Greedy Best-First Search
3. A* Search

The idea is quite simple, actually. There’s an AI agent, who has been provided the starting position and the goal state. The user must tell it which algorithm they want the agent to implement, depending upon that, the path is calculated.
Once the path is calculated, the agent constructs the path step by step, taking each direction towards the goal.

Note that the environment is fully observable, so the complete maze layout is already disclosed. 

One of the interesting parts of this project was to notice how differently each algorithm figured out the path and how the agent behaved. It also taught me that Hill Climbing with many times choose a locally promising decision which ends up causing its demise. 

It’s a very minor project, but I did it so I could perfectly connect the concepts of the theory with the implementation. 
