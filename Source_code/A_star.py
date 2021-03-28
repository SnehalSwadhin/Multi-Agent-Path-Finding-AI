'''
This file contains an implementation of the A* pathfinding algorithm for finding the shortest
path between two List_Items.
Instead of using a priority queue, the heapq library of python is used to create a Min-Heap,
which will be the open list. 
And whether a node has been explored/visited (i.e., added to the closed list) is stored in the
grid only, by using a boolean member variable (closed) to indicate the same.
'''

from heapq import *

grid = []
end = None

'''
 List_Item - Class to encapsulate the location of a Node, its equality, and its less-than criteria.
            This is required in order to use the heappush, heappop, and heapify functions from the
            heapq library.
'''
class List_Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __lt__(self, other):
        return grid[self.x][self.y].f < grid[other.x][other.y].f
 
'''
 Node - Class to encapsulate nodes of the state-space. It contains the coordinates of the grid-point,
        g-value (path-lenght from start), f-value (g-value + distance to end), parent of the node,
        and a boolean to indicate if the node has been closed. 
'''
class Node:
    def __init__(self, val, x, y, g = -1, f = -1, parent = None, closed = False):
        self.val = val
        self.x = x
        self.y = y
        self.g = g
        self.f = f
        self.parent = parent
        self.closed = closed

# inside_grid(x, y) - Function to check if the point (x, y) lies inside the grid boundaries.
def inside_grid(x, y):
    if x >= 0 and x < len(grid) and y >= 0 and y < len(grid[0]):
        return True
    else:
        return False

# insert_node(x, y, g, curr, open) - Function to insert a List_item into the open list with
#           the provided coordinates, g-value and parent as the node curr, passed as parameters.
def insert_node(x, y, g, curr, open):
    global grid
    global end

    # If the input coordinates are inside the grid and it is not an obstacle or closed node
    if inside_grid(x, y) and grid[x][y].val != '##' and not grid[x][y].closed:

        # If the node has not been explored before, i.e., its g-value is -1 (default)
        if grid[x][y].g == -1:
            grid[x][y].g = g
            grid[x][y].f = g + abs(x - end.x) + abs(y - end.y)
            grid[x][y].parent = curr
            heappush(open, List_Item(x, y))
        # Otherwise the node is alredy in open, but its g and f cost may need to be updated
        elif g < grid[x][y].g:
            # In case the new g-value is smaller than the old value, update - f, g, and parent
            grid[x][y].f -= grid[x][y].g - g
            grid[x][y].g = g
            grid[x][y].parent = curr

            # Heapify the list after updating the values
            heapify(open)

# A_star(maze, robot_start, destination) - The main function to find the shortest path from
#       start to end using the above helper functions.
def A_star(maze, robot_start, destination):
    global grid
    global end
    # Convert the maze into a matrix of nodes, whose f and g values remain to be calculated
    grid = []
    for i in range(0, len(maze)):
        grid.append([])
        for j in range(0, len(maze[0])):
            grid[i].append(Node(maze[i][j], i, j))


    start = List_Item(robot_start[0], robot_start[1])
    end = List_Item(destination[0], destination[1])

    # Set the f-value of the start node
    grid[start.x][start.y].f = abs(start.x - end.x) + abs(start.y - end.y)
    open = []
    heappush(open, start)

    # Defining the neighbourhood of a point to be and increase or deacrease in either the
    # x coordinate or the y cooedinate
    neighbourhood = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    # Loop while the open list is not empty
    while open != []:
        # Pop the top-most list item in open (i.e., the List-item with the lowest f-value)
        curr = heappop(open)

        if curr == end: # The end is reached
            break

        curr = grid[curr.x][curr.y]
        grid[curr.x][curr.y].closed = True
        
        # Using the state transformation rules, insert the neighbouring nodes into the open list
        for dx, dy in neighbourhood:
            x_, y_, g_ = curr.x + dx, curr.y + dy, curr.g + 1 
            # The g-value of any neighbour node will be 1 greater than the current node

            insert_node(x_, y_, g_, curr, open)

    # If end was not reached before emptying the open list
    if not curr == end:
        print("No Path")
        return []

    else:
        # Retrace and store the shortest path found using the above algorithm
        path = [(end.x, end.y)]
        n = grid[end.x][end.y].parent
        while n != None:
            path.append((n.x, n.y))
            n = n.parent

        # Reverse the list as we retraced the path from end to start
        path.reverse()
        return path