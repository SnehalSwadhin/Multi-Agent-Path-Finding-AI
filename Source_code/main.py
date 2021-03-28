'''
Multi-Agent Pathfinding and Planning
====================================
Details: Term Project for "Artificial Intelligence: Foundation and Application",
    (2021), Center of Excellence in AI, IIT Kharagpur.

Description: This program is an attempt at implementing multi-agent pathfinding
    for the scenario of a warehouse where multiple robots are used to pick-up and
    deliver items from one point to another. The robots are considered to move only
    one step at a time either in the vertical, or in the horizontal direction
    The main modules used for this program are -
    1) Task assignment - Assigning the task to robots in a way that minimizes the
            overall time taken.
    2) Path planning - Implementation of the A* algorithm for searching shortest path
            from a start to end point. Heuristic used is the manhattan distance between
            the two points.
    3) Conflict-Based Search - After all the paths are planned without considering
            collision, all conflicts are searched and resolved by preventing an agent
            from moving or moving it out of the way for an instant

Date: 28th March, 2021

Authors:
    Snehal Swadhin (19ME10067)
    Priyam Saha (19HS20030)
    Bhosale Ratnesh Sambhajirao (19MF10010)
'''

from os import system, name
from time import sleep
from A_star import A_star
from Assign_Task import assign_tasks, manhattan_dist
from conflict_based_search import CBS

''' 
print_maze(maze, AG) - Function to display the current state of the maze/grid, given
                       an array of agents and their current locations
'''
def print_maze(maze, AG):
    maze_copy = []
    # Making a acopy of the maze
    for i in maze:
        maze_copy.append([])
        for j in i:
            maze_copy[-1].append(j)

    # Marking all agent locations
    for agent in AG:
        (x, y) = agent.location
        maze_copy[x][y] = "R" + str(agent.name)

    # Printing the maze (a 2D list) in a clean manner to visualize the current state
    print('\n'.join(' '.join(i) for i in maze_copy))
    
# clear_screen() - Clears the output terminal
def clear_screen():
    if name == 'nt': 
        _ = system('cls')  # For Windows, the command used is 'cls'
    else: 
        _ = system('clear')  # For Linux, the command used is 'clear'


# Agent - A class for defining an agent, having a name, current location, and final destination
class Agent:
    def __init__(self, name, location, end):
        self.name = name
        self.location = location
        self.end = end

    # clone(self) - Function to return a clone of the instance of class which calls it
    def clone(self):
        return Agent(self.name, self.location, self.end)

'''
arrange_data(bots, tasks, blocks, height, width) - Function to arrange the input data
    into a maze or 2D list for easy traversal and searching. Inputs are provided in
    the form of a list of robots (with start and end locations), a list of tasks (with 
    pickup and drop locations), a list of blocks/obstacles in the maze/grid, and the
    dimensions of the maze.
'''
def arrange_data(bots, tasks, blocks, height, width):
    maze = [[ '  ' for i in range(width)] for j in range(height)]
    for i, j in blocks:
        maze[i][j] = '##'

    for i, ((a1, a2), (b1, b2)) in enumerate(bots):
        maze[b1][b2] = 'E' + str(i + 1)

    for i, ((a1, a2), (b1, b2)) in enumerate(tasks):
        maze[a1][a2] = 'P' + str(i + 1)
        maze[b1][b2] = 'D' + str(i + 1)

    return maze


'''
main(height, width, bots, tasks, blocks) - The main function which calls all the helper
    functions for creating the maze and finding the plan for carrying out all the tasks.
'''
def main(height, width, bots, tasks, blocks):
    # Creating a list of Agent objects from the list of input bot locations
    AG = [Agent(i + 1, a, b) for i, (a, b) in enumerate(bots)]

    # Arranging all the data into a maze for easy traversal and searching
    maze = arrange_data(bots, tasks, blocks, height, width)

    ''' 
     Calculating and adding the heuristic length or time required for completing each task
     Note - As the agents cannot move diagonally, and they can move only one step at a time,
     the length of any path will be same as the time required to traverse it.
    '''
    for task in tasks:
        task.append(manhattan_dist(task[0], task[1]))
    '''
     Sorting the tasks in descending order of predicted path lengths.
     This is done in order to make the task assignment to different agents more efficient.
     The longer tasks are assigned first and consequently other tasks are assigned to agents
     such that max(time taken by agent) is minimum
    '''
    tasks = sorted(tasks, key = lambda x: x[2], reverse = True)
    

    paths = [] # A list to store the paths to be followed by each agent
    max_path_len = 0

    # Assigning tasks to agents and storing the list of task assigned in the following list
    assigned = assign_tasks(tasks, AG, len(maze)*len(maze[0]))

    # Finding and storing the sortest paths the agents have to follow to complete their
    # respective assigned tasks
    for i, agent in enumerate(AG):
        paths.append([])

        curr_task = assigned[i][0] # The first task to be done by ith agent

        # Shortest path from agent's start location to pick-up location of first task
        paths[-1] = A_star(maze, agent.location, tasks[curr_task][0])
        paths[-1] = paths[-1][:-1]  # Removing the end point of the path to prevent 
                                    # it from being added twice

        for j in range(len(assigned[i])):
            curr_task = assigned[i][j] # Current task to be performed

            # Shortest path from pick-up to destination of tesk-item
            paths[-1] += A_star(maze, tasks[curr_task][0], tasks[curr_task][1])
            paths[-1] = paths[-1][:-1]  # Removing the end point of the path to prevent 
                                        # it from being added twice

            if(j < len(assigned[i])-1): # For all tasks except the last one
                next_task = assigned[i][j+1]

                # Add shortest path from destination of current task to start of next task
                paths[-1] += A_star(maze, tasks[curr_task][1], tasks[next_task][0])
                paths[-1] = paths[-1][:-1]  # Removing the end point of the path to prevent 
                                            # it from being added twice
            else:
                # Add shortest path to the end location of agent as no more tasks are to be performed
                paths[-1] += A_star(maze, tasks[curr_task][1], agent.end)

        # Store the largest path length among all agents, i.e max(Time taken by agent)
        if len(paths[-1]) > max_path_len:
            max_path_len = len(paths[-1])

    # After all the paths are planned for each agent, find and resolve all conflicts (or collision)
    CBS(maze,paths, max_path_len)

    # Revising the largest path length among all agents
    for i in range(len(paths)):    
        if len(paths[i]) > max_path_len:
            max_path_len = len(paths[i])

    '''
     For visualizing the traversal, all agents with paths shorter than the largest path should stay
     at their end locations while other agents finish their tasks.
     Adding extra path-points at the end of their paths for all such agents.
    '''
    for p in paths:
        if len(p) < max_path_len:
            p += [p[-1]]*(max_path_len - len(p) + 1)
        print(p)

    # Displaying the traversal of all agents
    for i in range(max_path_len):
        # Move all agents to their path-points at the ith time step
        for j in range(len(AG)):
            AG[j].location = paths[j][i]

        # Clearing the screen for removing the state displayed at previous time-step
        clear_screen()
        print_maze(maze, AG)

        # Wait for some time before moving to the next time step
        sleep(0.2)
 
# Defining the list of bots with their start and end points   
bots = [
    #   R       E
    [(4, 0), (4, 4)],
    [(8, 4), (1, 9)]
]

# Defining the list of task with their pickup and drop locations
tasks = [
    #   P        D
    [(4, 12), (4, 11)],
    [(10, 1), (5, 12)],
    [(5, 15), (9, 1)]
]

# Defining the locations of obstacles present in the maze/grid
blocks = [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5)]

height = 11
width = 18

# Calling the main(_) function which shows the traversal of above defined bots
# for carying out the tasks provided.
main(height, width, bots, tasks, blocks)
