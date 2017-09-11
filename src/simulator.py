import environment
import agent
from astar import Astar

class Simulator:

    def __init__(self):
        self.envInstance = environment.Environment(30, 4, 4)
        self.envInstance.generate_env()
        self.visitedCells = [[False for i in range(self.envInstance.dimension)] for j in range(self.envInstance.dimension)]
        self.agent = agent.Agent(0, 0, 100, self.envInstance.calculate_initial_capacity())
        self.envInstance.set_cell_content(self.agent.x, self.agent.y, "A")

    def go_through_environment(self):

        stack = []

        flag = True
        while stack or flag:
            allVisited = True
            flag = False

            currX, currY = self.agent.get_position()

            currCell = self.envInstance.get_cell(currX, currY)
            neighbors = currCell.get_neighbors()
  
            for nbCell in neighbors:
                nbX, nbY = nbCell.get_position()

                if self.visitedCells[nbX][nbY] == False and nbCell.get_content() not in self.envInstance.forbidden_cell():           
                    allVisited = False
                    stack.append(currCell)

                    self.visitedCells[nbX][nbY] = True
                    self.envInstance.set_cell_content(currX, currY, " ")
                    self.envInstance.set_cell_content(nbX, nbY, "A")

                    self.agent.set_position(nbX, nbY)

                    break
              
            # Go back to previous cell
            if allVisited is True:
                prevCell = stack.pop()
                prevX, prevY = prevCell.get_position()

                self.envInstance.set_cell_content(currX, currY, " ")
                self.envInstance.set_cell_content(prevX, prevY, "A")
                self.agent.set_position(prevX, prevY)


    def get_shortest_distance_to_recharge(self):
        rechargePoints = self.envInstance.get_recharge_points()

        firstPoint = rechargePoints[0]
        bestValue = self.heuristic(self.agent.x, self.agent.y, firstPoint[0], firstPoint[1])

        for point in rechargePoints:
            auxValue = self.heuristic(self.agent.x, self.agent.y, point[0], point[1])

            if (auxValue < bestValue):
                bestValue = auxValue
        return bestValue
    
    def get_shortest_distance_to_trash_can(self):
        trashCanPoints = self.envInstance.get_trash_can_points()

        firstPoint = self.trashCanPoints[0]
        bestValue = self.heuristic(self.agent.x, self.agent.y, firstPoint[0], firstPoint[1])

        for point in trashCanPoints:
            auxValue = self.heuristic(self.agent.x, self.agent.y, point[0], point[1])

            if (auxValue < bestValue):
                bestValue = auxValue
        return bestValue

    def get_nearbiest_recharge_point(self):
        values = {}
        rechargePoints = envInstance.get_recharge_points()

        for point in rechargePoints:
            values[self.heuristic(self.agent.x, self.agent.y, point[0], point[1])] = (point[0], point[1])
        return values[min(values)]

    def get_nearbiest_trash_can_point(self):
        values = {}
        trashCanPoints = self.envInstance.get_trash_can_points()

        for point in trashCanPoints:
            values[self.heuristic(self.agent.x, self.agent.y, point[0], point[1])] = (point[0], point[1])
        return values[min(values)]

    def heuristic(self, posX, posY, goalX, goalY):
        return abs(goalX - posX) + abs(goalY - posY)

if __name__ == "__main__":
    sim = Simulator()
    
    sim.envInstance.print_env()
    sim.go_through_environment()
    sim.envInstance.print_env()