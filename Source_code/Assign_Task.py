'''
 This file contains the algorithm for assigning all the tasks to different agents
 while trying to minimize the maximum time required by any particular agent
'''

'''
 Dynamic programming table to store the predicted time required (heuristic) for
 travelling between a start and end location. This is done to preserve computation
 time for queries previously calculated
'''
time_req = {}

'''
Bot - A Class to encapsulate an agent, the tasks assigned to it, and the predicted
		time it spends in completing those tasks.
'''
class Bot:
	def __init__(self, agent, tasks, time_spent = 0):
		self.agent = agent
		self.tasks = tasks
		self.time_spent = time_spent
	
	# add_task(self, task) - Member function to add a task an the instance of Bot class.
	def add_task(self, task):
		self.tasks.append(task)

# manhattan_dist(start, end) - Returns the manhattan distance between two points,
#				which is the same as the time required to travel the distance.
def manhattan_dist(start, end):
	global time_req

	# If query is not present in the DP table (time_req), Then calculate and store 
	# the distance in the table.
	if (start, end) not in time_req:
		time_req[(start, end)] = abs(start[0] - end[0]) + abs(start[1] - end[1])

	return time_req[(start, end)]

def assign_tasks(tasks, AG, size_of_maze):
	global time_req

	robots = [] # List of Bot objects containing each agent and their tasks
	for agent in AG:
		# Bot object is created using clones of the agents, as we don't want these any changes to
		# be reflected on the actual Agent objects.
		robots.append(Bot(agent.clone(), [])) # Initially, no task is assigned to any agent

	for i, t in enumerate(tasks):
		best_bot = 0 # Assuming any bot is the best one to be performing the current task t (i.e ith task)
		min_time_spent = size_of_maze 	# Assuming a large value of the minimum time in
										# which task t can be finished
		
		for j, bot in enumerate(robots):
			# Calculate time required by jth bot to finish task t (i.e ith task).
			# i.e., the time spent by bot till now + time required to move to pick-up location + the
			# time required for the task itself
			curr_time_spent = bot.time_spent + manhattan_dist(bot.agent.location, t[0]) + t[2]
			if(curr_time_spent < min_time_spent):
				min_time_spent = curr_time_spent
				best_bot = j

		robots[best_bot].add_task(i) # Assigning current task to the best_bot
		robots[best_bot].agent.location = t[1] # Change the best_bot's location to destination of current task
		robots[best_bot].time_spent += min_time_spent # Update the time spent by this bot till now

	# Create a list of all task assignments and return the list
	assigned = []
	for bot in robots:
		assigned.append(bot.tasks)
	return assigned