import enum

class Direction(enum.Enum):
	NORTH 		= (0, -1)
	SOUTH 		= (0, 1)
	EAST		= (1, 0)
	WEST		= (-1, 0) 
	NORTHEAST 	= (1, -1)
	NORTHWEST 	= (-1, -1)
	SOUTHEAST 	= (1, 1)
	SOUTHWEST 	= (-1, 1)

	def __init__(self, x, y):
		self.x = x
		self.y = y