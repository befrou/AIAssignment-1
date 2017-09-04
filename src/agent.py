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
