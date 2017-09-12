import environment
import agent
import sys
import time
from heapq import heappush, heappop
from itertools import count

class Simulator:

    def __init__(self, agentEnergy, agentCapacity, dimension, rechargePoints, trashCanPoints):
        self.envInstance = environment.Environment(dimension, rechargePoints, trashCanPoints)
        self.envInstance.generate_env()
        self.visitedCells = [[False for i in range(self.envInstance.dimension)] for j in range(self.envInstance.dimension)]
        self.agent = agent.Agent(0, 0, agentEnergy, agentCapacity)
        self.agent.set_limit_energy(self.envInstance.dimension + 5)

    def go_through_environment(self):
        stack = []

        flag = True

        print("Hey. I'm a robot. My initial position is " + str(self.agent.get_position()))
        print("My initial energy is " + str(self.agent.energy))
        print("My initial capacity is " + str(self.agent.originalCapacity))
        print("I need to recharge whenever my energy has been " + str(self.agent.energyLimit))
        print("\n##############################################")
        while stack or flag:
            allVisited = True
            flag = False

            #Get position of agent
            currX, currY = self.agent.get_position()

            #Get cell of this position
            currCell = self.envInstance.get_cell(currX, currY)

            #If agent have enough energy
            if self.agent.energy > self.agent.energyLimit:

                #Decrease the energy at new visited cell
                self.agent.decrease_energy()
                self.visitedCells[currX][currY] = True

                #If cell is dirty test if agent has capacity to clean
                if self.envInstance.cell_is_dirty(currX, currY):
                    if self.agent.has_capacity():
                        # Clean cell
                        self.envInstance.set_cell_content(currX, currY, " ")
                        self.agent.decrease_capacity()
                    else:
                        print("\nCapacity full. I have " + str(self.agent.originalCapacity) + " trash bags with me.")

                        #Find the neabiest trashcan point
                        nearbiestTrashCan = self.get_nearbiest_trash_can_point()
                        trashCan = self.envInstance.get_cell(nearbiestTrashCan[0], nearbiestTrashCan[1])

                        #Run A* algorithm and move the agent to nearbiest trashcan
                        pathToTrashCan = self.astar(currCell, trashCan)

                        #Walk to the goal
                        for cell in pathToTrashCan:
                            #Check the energy each step while searching for a trashcan
                            if self.agent.energy <= self.agent.energyLimit:
                                #If energy is low, go to the nearest charging station
                                print("Oh no. Battery is low while running into a trashcan. Going to a charging station now.")
                                self.go_to_charging_station(currCell)

                            #If is a trashcan point drop the dirt and fill the capacity
                            if cell.get_content() == "T":
                                print("Emptying my backpack at point: " + str((cell.x, cell.y)))
                                self.agent.fill_capacity()
                            else:
                                self.agent.set_position(cell.x, cell.y)
                                self.agent.decrease_energy()

                        #Back to previous position
                        backToPrevCoord = pathToTrashCan[::-1]
                        for cell in backToPrevCoord:
                            self.agent.set_position(cell.x, cell.y)
                            self.agent.decrease_energy()

                        #Set the agent position again
                        newX, newY = self.agent.get_position()

                        #Clean the dirt and decrease the capacity
                        self.envInstance.set_cell_content(currX, currY, " ")
                        self.agent.decrease_capacity()

                #Get the neighbors of the current cell
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
            else:
                print("\nBattery low. I have " + str(self.agent.energy) + " of energy remaining.")

                self.go_to_charging_station(currCell)

        print("\n#############################################")

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


    def go_to_charging_station(self, currCell):
        #Find the neabiest recharge point
        nearbiestRechargePoint = self.get_nearbiest_recharge_point()
        rechargePoint = self.envInstance.get_cell(nearbiestRechargePoint[0], nearbiestRechargePoint[1])

        # Run A* algorithm and move the agent to nearbiest recharge point
        pathToRechargePoint = self.astar(currCell, rechargePoint)

        #Walk to the goal
        for cell in pathToRechargePoint:
            # If is a recharge point recharge the agent energy
            if cell.get_content() == "R":
                print("Recharging my energy at point: " + str((cell.x, cell.y)))
                #Debug mode to check recharging
                #self.envInstance.print_env()
                self.agent.recharge_energy()
            else:
                self.agent.set_position(cell.x, cell.y)
                self.agent.decrease_energy()

        #Back to previous position
        backToPrevCoord = pathToRechargePoint[::-1]
        for cell in backToPrevCoord:
            self.agent.set_position(cell.x, cell.y)

        #Set the agent position again
        newX, newY = self.agent.get_position()

if __name__ == "__main__":

    if len(sys.argv) < 5:
        print("Invalid command. Try this: python3 simulator.py energy capacity dimension rechargePoints trashcanPoints")
        exit()

    try:
        agentEnergy = int(sys.argv[1])
        agentCapacity = int(sys.argv[2])
        dimension = int(sys.argv[3])
        rechargePoints = int(sys.argv[4])
        trashCanPoints = int(sys.argv[5])
    except:
        print("Error. The energy, capacity and dimension values must be a number.")
        exit()

    if agentEnergy <= 0 or agentCapacity <= 0:
        print("Error. The energy and capacity and dimension values must be greater than zero.")
        exit()

    # (+ 6) Because the energy limit is based on the (dimension + 5). So the agent needs at least 1 energy
    if agentEnergy < (dimension + 6):
        print("The agent energy must be greater than the size of the map + 5 (Energy Limit).")
        exit()

    start_time = time.time()
    sim = Simulator(agentEnergy, agentCapacity, dimension, rechargePoints, trashCanPoints)
    sim.envInstance.print_env()
    sim.go_through_environment()
    sim.envInstance.print_env()
    print("Hey! I finished my job in %s seconds. :)" % round(float(time.time() - start_time), 3))