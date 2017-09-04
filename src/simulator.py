from environment import Environment, Direction

class Simulator:
	
	def __init__(self):
		self.envInstance = Environment(15, 4, 5)
		self.envInstance.generate_env()
		self.visitedPositions = [[False for i in range(self.envInstance.dimension)] for j in range(self.envInstance.dimension)]

	def go_through_environment(self):
		dirs = list(Direction)
		mapOppositeDir = {"NORTH":Direction.SOUTH, "SOUTH":Direction.NORTH, "EAST":Direction.WEST, "WEST":Direction.EAST, "SOUTHEAST":Direction.NORTHWEST, "NORTHWEST":Direction.SOUTHEAST, "SOUTHWEST":Direction.NORTHEAST, "NORTHEAST":Direction.SOUTHWEST}
		stack = [] # This stack stores the opposite directions of the moves made by the agent (this way the agent can trace his steps back to its first position) 
	
		self.visitedPositions[0][0] = True

		flag = True # Stack starts empty so use this flag to enter loop

		while stack or flag:

			flag = False
			allVisited = True

			for val in dirs:
				newCoord = self.envInstance.valid_move(val)

				# Haven't visited position yet
				if newCoord and self.visitedPositions[newCoord[0]][newCoord[1]] == False:
				
					allVisited = False
					stack.append(mapOppositeDir[val.name])
							
					self.visitedPositions[newCoord[0]][newCoord[1]] = True
					self.envInstance.matrix[self.envInstance.agent.x][self.envInstance.agent.y] = " "
					self.envInstance.agent.move(val)
					self.envInstance.matrix[newCoord[0]][newCoord[1]] = "A"

					break
			
			# Go back to previous coordinate
			if allVisited == True:
				prevCoord = stack.pop()
				self.envInstance.matrix[self.envInstance.agent.x][self.envInstance.agent.y] = " "
				self.envInstance.agent.move(prevCoord)
				self.envInstance.matrix[self.envInstance.agent.x][self.envInstance.agent.y] = "A"


	def run_env(self):
		self.go_through_environment()

if __name__ == "__main__":
	sim = Simulator()
	sim.envInstance.print_env()
	sim.go_through_environment()
	sim.envInstance.print_env()