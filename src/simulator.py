import environment
import agent
from heapq import heappush, heappop
from itertools import count

class Simulator:

    def __init__(self):
        self.envInstance = environment.Environment(10, 4, 4)
        self.envInstance.generate_env()
        self.visitedCells = [[False for i in range(self.envInstance.dimension)] for j in range(self.envInstance.dimension)]
        self.agent = agent.Agent(0, 0, 100, 10)
        # self.envInstance.set_cell_content(self.agent.x, self.agent.y, "A")

    def print_o(self):
        print("\n\nX X", end = " ")
        for j in range(self.envInstance.dimension):
            print("X", end=" ")

        print("")

        for i in range(self.envInstance.dimension):
            print("X ", end="")
            for j in range(self.envInstance.dimension):
                if (i, j) == self.agent.get_position():
                    print("A", end=" ")
                else:    
                    position = self.envInstance.get_array_position(i, j)
                    print(str(self.envInstance.matrix[position].get_content()), end=" ")
            print("X")

        print("X X", end=" ")
        for j in range(self.envInstance.dimension):
            print("X", end=" " )
        print("\n\n")


    def go_through_environment(self):

        stack = []

        flag = True
        while stack or flag:
            allVisited = True
            flag = False

            currX, currY = self.agent.get_position()
            self.visitedCells[currX][currY] = True

            currCell = self.envInstance.get_cell(currX, currY)
            
            if self.envInstance.cell_is_dirty(currX, currY):
                if self.agent.has_capacity():
                    # Clean cell
                    self.envInstance.set_cell_content(currX, currY, " ")
                    self.agent.decrease_capacity()
                else:
                    goalCoord = self.get_nearbiest_trash_can_point()
                    goal = self.envInstance.get_cell(goalCoord[0], goalCoord[1])    

                    #Run A* algorithm and move the agent to nearbiest trashcan
                    pathToTrashCan = self.astar(currCell, goal)
                    for cell in pathToTrashCan:
                        self.agent.set_position(cell.x, cell.y)
                        #If is a trashcan point drop the dirt and fill the capacity
                        if cell.get_content() == "T":
                            self.agent.fill_capacity()
                    
                    #Back to previous position
                    backToPrevCoord = pathToTrashCan[::-1]
                    for cell in backToPrevCoord:
                        self.agent.set_position(cell.x, cell.y)
                    #Set the agent position again
                    newX, newY = self.agent.get_position()     
                    
                    #Clean the dirt and decrease the capacity
                    self.envInstance.set_cell_content(currX, currY, " ")
                    self.agent.decrease_capacity()       

            neighbors = currCell.get_neighbors()

            for nbCell in neighbors:
                nbX, nbY = nbCell.get_position()

                if (self.visitedCells[nbX][nbY] == False and 
                    nbCell.get_content() not in self.envInstance.forbidden_cell()):

                    allVisited = False
                    stack.append(currCell)

                    self.agent.set_position(nbX, nbY)
                    self.agent.decrease_energy()

                    break
              
            # Go back to previous cell
            if allVisited is True:
                prevCell = stack.pop()
                prevX, prevY = prevCell.get_position()
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

        firstPoint = trashCanPoints[0]
        bestValue = self.heuristic(self.agent.x, self.agent.y, firstPoint[0], firstPoint[1])

        for point in trashCanPoints:
            auxValue = self.heuristic(self.agent.x, self.agent.y, point[0], point[1])

            if (auxValue < bestValue):
                bestValue = auxValue
        return bestValue

    def get_nearbiest_recharge_point(self):
        values = {}
        rechargePoints = self.envInstance.get_recharge_points()

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

    def astar(self, start, goal):
        visited = {}
        computedInfo = {}

        push = heappush
        pop = heappop

        c = count()
        queue = [(0, next(c), start, 0, None)]

        while queue:
            # Pop the smallest item from queue.
            _, __, current, dist, previous = pop(queue)

            if current == goal:
                path = [current]
                cell = previous
                while cell is not None:
                    path.append(cell)
                    cell = visited[cell]
                path.reverse()
                return path

            if current in visited:
                continue

            visited[current] = previous
            for neighbor in current.get_neighbors():
                if (neighbor == goal):
                    pass
                elif (neighbor in visited or
                    neighbor.get_content() in self.envInstance.forbidden_cell()):
                    
                    continue

                neighborCost = dist + 1
                if neighbor in computedInfo:
                    prevCost, h = computedInfo[neighbor]

                    if prevCost <= neighborCost:
                        continue
                else:
                    h = self.heuristic(neighbor.x, neighbor.y, goal.x, goal.y)
                
                computedInfo[neighbor] =  neighborCost, h
                push(queue, (neighborCost + h, next(c), neighbor, neighborCost, current))




if __name__ == "__main__":
    sim = Simulator()
    sim.envInstance.print_env()
    sim.go_through_environment()
    sim.envInstance.print_env()