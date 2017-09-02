import environment as env

class Agent:

	def __init__(self, x, y, energy, dirtCapacity):
		self.energy = energy
		self.dirtCapacity = dirtCapacity
		self.x = x
		self.y = y

	def move(self, direction):
		self.x += direction.x
		self.y += direction.y

		return self.x, self.y

	def go_through_environment(self, environment):
		dirs = list(env.Direction)
		queue = []

		for val in dirs:
			if self.valid_move(environment.matrix, val):
				queue.append(val)
		
		#for val in queue:

	
	def valid_move(self, matrix, direction):
		new_x = self.x + (direction.x)
		new_y = self.y + (direction.y)

		if new_x >= 0 and new_y >= 0:
			if (matrix[new_x][new_y] != "W" and
				matrix[new_x][new_y] != "R" and
				matrix[new_x][new_y] != "T"):

				return True
			else:
				return False