import random
import math
import direction

class Environment:

	def __init__(self, dimension, rechargePoints, trashCans):
		self.dimension = dimension
		self.dirtPercentage = random.randint(40, 85)
		self.dirt = 0
		self.rechargePoints = rechargePoints
		self.trashCans = trashCans
		self.matrix = [None] * (self.dimension * self.dimension)
		self.recharge_points = []
		self.trashcans_points = []

	def get_cell(self, x, y):
		return self.matrix[self.get_array_position(x, y)]

	def forbidden_cell(self):
		return ["W", "T", "R"]

	def get_dimension(self):
		return self.dimension
	
	def calculate_initial_capacity(self):
		return int(round(pow(self.dimension, 2) * 0.8, 2) / 2)
	
	def get_cell_content(self, x, y):
		return self.matrix[self.get_array_position(x, y)]
	
	def cell_is_dirty(self, x, y):
		return self.matrix[self.get_array_position(x, y)] == "d"
	
	def get_recharge_points(self):
		return self.recharge_points
	
	def get_trash_can_points(self):
		return self.trashcans_points

	def set_cell_content(self, x, y, content):
		position = self.get_array_position(x, y)
		self.matrix[position].set_content(content)

	# Allocate trash cans, recharge points and dirt
	def allocate_points_of_interest(self):
		totalPositions = pow(self.dimension, 2)
		occupiedPositions = 1

		aux = 0
		while aux < self.rechargePoints:
			i = random.randint(3, (self.dimension - 4))
			
			left_or_right = random.randint(0, 1)

			if left_or_right == 0:
				j_ini = 0
				j_end = 2
			else:
				j_ini = self.dimension - 3
				j_end = self.dimension - 1

			j = random.randint(j_ini, j_end)
			position = self.get_array_position(i, j)

			if self.matrix[position].get_content() == " ":
				aux = aux + 1
				self.matrix[position].set_content("R")
				self.recharge_points.append((i, j))
				occupiedPositions += 1

		aux = 0
		while aux < self.trashCans:
			i = random.randint(3, (self.dimension - 4))
			
			left_or_right = random.randint(0, 1)

			if left_or_right == 0:
				j_ini = 0
				j_end = 2
			else:
				j_ini = self.dimension - 3
				j_end = self.dimension - 1

			j = random.randint(j_ini, j_end)
			position = self.get_array_position(i, j)

			if self.matrix[position].get_content() == " ":
				aux = aux + 1
				self.matrix[position].set_content("T")
				self.trashcans_points.append((i, j))
				occupiedPositions += 1

		walls = (4 + (self.dimension - 4) * 2)
		occupiedPositions += walls

		self.dirt = math.floor((self.dirtPercentage * (totalPositions - occupiedPositions)) /  100)

		print("\nTotal positions in matrix: " + str(totalPositions))
		print("Occupied positions in matrix: " + str(occupiedPositions))
		print("Dirt percentage: " + str(self.dirtPercentage) + "%")
		print("Number of dirt positions: " + str(self.dirt))

		aux = 0
		while aux < self.dirt:
			i = random.randint(0, self.dimension - 1)
			j = random.randint(0, self.dimension - 1)

			position = self.get_array_position(i, j)

			if self.matrix[position].get_content() == " ":
				self.matrix[position].set_content("d")
				aux = aux + 1

	def generate_env(self):
		directions = list(direction.Direction)
		for i in range(self.dimension):
			for j in range(self.dimension):
				position = self.get_array_position(i, j)
				content = self.get_position_content(i, j)
				
				self.matrix[position] = Cell(i, j, content)	

		for i in range(self.dimension):
			for j in range(self.dimension):
				currPosition =  self.get_array_position(i, j)
				currCell = self.matrix[currPosition]

				for d in directions:
					nX = i + d.x
					nY = j + d.y

					if (nX >= 0 and nX < self.dimension and
						nY >= 0 and nY < self.dimension):

						nPosition = self.get_array_position(nX, nY)
						currCell.add_neighbor(self.matrix[nPosition])
		# print(self.matrix[self.get_array_position(5, 2)].get_neighbors())
		# exit()
		self.allocate_points_of_interest()


	def get_array_position(self, i, j):
		return i * (self.dimension - 1) + j

	def get_position_content(self, i, j):
		if i == 2:
			if j == 2  or j == 3:
				return "W"
			if j == (self.dimension - 3)  or j == (self.dimension - 4):
				return "W"

		elif i == self.dimension - 3:
			if j == 2  or j == 3:
				return "W"
			if j == (self.dimension - 3)  or j == (self.dimension - 4):
				return "W"
		elif i >= 2 and i <= (self.dimension - 3):
			if j == 3 or j == (self.dimension - 4):
				return "W"
		return " "

	def print_env(self):
		print("\n\nX X", end = " ")
		for j in range(self.dimension):
			print("X", end=" ")

		print("")

		for i in range(self.dimension):
			print("X ", end="")
			for j in range(self.dimension):
				position = self.get_array_position(i, j)
				print(str(self.matrix[position].get_content()), end=" ")
			print("X")

		print("X X", end=" ")
		for j in range(self.dimension):
			print("X", end=" " )
		print("\n\n")


class Cell:
	def __init__(self, x, y, content):
		self.x = x
		self.y = y
		self.parent = None
		self.neighbors = []
		self.content = content

	def get_position(self):
		return self.x, self.y

	def get_content(self):
		return self.content

	def set_content(self, content):
		self.content = content

	def add_neighbor(self, nb):
		self.neighbors.append(nb)

	def get_neighbors(self):
		return self.neighbors

if __name__ == "__main__":
    env = Environment(15, 3, 3)
    env.generate_env()
    env.print_env()
