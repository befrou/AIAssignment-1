from environment import Environment, Direction
import agent

class Simulator:
	
	def __init__(self):
		self.envInstance = Environment(15, 4, 5)
		self.envInstance.generate_env()

if __name__ == "__main__":
	sim = Simulator()
	sim.envInstance.run_env()