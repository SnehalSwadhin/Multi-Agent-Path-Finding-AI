# Multi-Agent-Path-Finding-AI
This repository contains the submission for the assignment on search methods for the course "Artificial Intelligence: Foundation and Application (2021)", Center of Excellence in AI, IIT Kharagpur.

## Description
The purpose of this project is to have complete a list of given tasks of delivering items from pickup and drop locations using multiple agents or robots.
All the tasks are to be done optimally in order to minimize the maximum time taken by a particular agent. For that, all the agents must be assigned their tasks in a way that fulfills that goal.

## User Mannual
- All the parameters of the problem have been defined at the end of the file and passed to the main(_) function.
- To run the algorithm, simply run the command "python main.py" inside the Source_code folder.
  (Note - All the files inside the Source_code folder must be present for running the algorithm)
- The input to the algorithm can be changed by changing the following variables defined at the end of 'main.py'.
- All locations have been defined as (row no., column no.)
- The warehouse has been defined using a list of locations of blocks/obstacles (Variable name -> blocks), along with the height (Variable name -> height) and width (Variable name ->width) of the warehouse.
  By changing these three variables, a user can define their warehouse layout.
- The Robots have been defined as a list of their start and end locations (Variable name -> bots).
  Syntax used to define robots : [(R(i).x, R(i).y), (E(i).x, E(i).y)]
  where, 	R(i) = Start location of ith robot.
  			R(i).x = Row number of R(i)
  			R(i).y = Column number of R(i)
  			E(i) = End location of ith robot.
  			E(i).x = Row number of E(i)
  			E(i).y = Column number of E(i)
- The Tasks have been defined as a list of their pick-up and destination locations (Variable name -> tasks).
  Syntax used to define robots : [(P(i).x, P(i).y), (D(i).x, D(i).y)]
  where, 	P(i) = Pick-up location of ith robot.
  			P(i).x = Row number of P(i)
  			P(i).y = Column number of P(i)
  			D(i) = Destination location of ith robot.
  			D(i).x = Row number of D(i)
  			D(i).y = Column number of D(i)
- After setting these variables to your liking, you can execute the code in 'main.py' by running the command "python main.py" inside the Source_code folder.

## Documentation
The logic and implementation of the entire project has been explained in an attached documentation (Documentation.pdf).

## Limitations
The most apparant feature that has been left out from the problem statement is the use of temperory storage locations. There is currently no way to indicate or make use of temperory storage locations. That is because we were unable to figure out a way of implementing the same and make use of them optimally.