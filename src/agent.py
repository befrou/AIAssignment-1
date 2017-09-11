class Agent:

    def __init__(self, x, y, energy, capacity):
        self.energy = energy
        self.capacity = capacity
        self.energyLimit = energy
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def set_position(self, x, y):
        self.x = x
        self.y = y
    
    def set_limit_energy(self, newLimit):
        self.energyLimit = newLimit * 2

    def has_capacity(self):
        return self.capacity > 0    
    
    def decrease_capacity(self):
        self.capacity -= 1
    
    def decrease_energy(self):
        self.energy -= 2