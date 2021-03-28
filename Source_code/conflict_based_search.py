'''
This file contains the conflict-based search algorithms for searching and avoiding collision
among agents while traversing theor already planned paths.
'''

'''
available_spot(curr_location, avoid, maze) - Function to return any available spot for an agent
		to move to in order to avoid collision in the next time step. The agent has to avoid any
		obstacles "##" and the points passed in the "avoid" list passed as a parameter.
'''
def available_spot(curr_location, avoid, maze):
	neighbourhood = [(-1, 0), (0, -1), (0, 1), (1, 0)]
	for dx, dy in neighbourhood:
		next_spot = (curr_location[0] + dx, curr_location[1] + dy)
		if maze[next_spot[0]][next_spot[1]] != '##' and next_spot not in avoid:
			return next_spot

'''
CBS(maze, paths, max_path_len) - Function to search for conflicts in the paths of all agents
		and add appropriate nodes/path-points in the path of one of the involved agents for
		avoiding that conflict.
		Given a conflict, the agent that has more "Slack" is selected to wait or move out of the
		the way and give passage for the other agent.
		"Slack" is a term used to refer to the time wasted by an agent after it has completed its
		own task, and is waiting for other agents to finish theirs
'''
def CBS(maze, paths, max_path_len):
	# Check for conflict at each time-step
	for time in range(max_path_len-1):
		# Loop for all agents
		for i in range(len(paths)):
			if (time >= len(paths[i])-1):
				continue
			# Loop for all agents after the ith agent 
			for j in range(i+1, len(paths)):
				if (time >= len(paths[j])-1):
					continue
				# If both ith and jth agent will be at the same point in the next time-step
				if paths[i][time+1] == paths[j][time+1]:
					# Select the agent with more slack and prevent it from moving to the point if collision
					if len(paths[j]) < len(paths[i]):
						# Add a path-point in the next time-step to wait at the same location
						paths[j] = paths[j][:time+1] + [paths[j][time]] + paths[j][time+1:]
					else:
						# Same logic applied for the other agent
						paths[i] = paths[i][:time+1] + [paths[i][time]] + paths[i][time+1:]

				# If ith and jth agent will exchange positions in the next time-step
				elif paths[i][time] == paths[j][time+1] and paths[i][time+1] == paths[j][time]:
					# Select the agent with more slack and move it out of the way for allowing the other
					# agent to move according to its planned path
					if len(paths[j]) < len(paths[i]):
						# Avoid going to the current location of the other agent, as that is what caused the conflict
						avoid = [paths[i][time]]

						# If the other agent's path does not end after the next time-step
						if time+2 < len(paths[i]):
							# Avoid the point which the other agent will go to in the next to next time-step
							avoid.append(paths[i][time+2])

						next_spot = available_spot(paths[j][time], avoid, maze) # Find an available spot to move to

						# Add a path point to move to the available spot for avoiding collision, and another to
						# move back to the point it was earlier.
						paths[j] = paths[j][:time+1] + [next_spot] + [paths[j][time]] + paths[j][time+1:]
					else:
						# Same logic applied for the other agent
						avoid = [paths[j][time]]
						if time+2 < len(paths[j]):
							avoid.append(paths[j][time+2])
						next_spot = available_spot(paths[i][time], avoid, maze)
						paths[i] = paths[i][:time+1] + [next_spot] + [paths[i][time]] + paths[i][time+1:]