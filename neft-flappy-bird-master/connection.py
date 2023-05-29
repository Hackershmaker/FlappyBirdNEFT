import random

class Connection:
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node  # The node where the connection originates
        self.to_node = to_node  # The node where the connection ends
        self.weight = weight  # The weight of the connection

    def mutate_weight(self):
        if random.uniform(0, 1) < 0.1:
            # Randomly assigns a completely new weight between -1 and 1
            self.weight = random.uniform(-1, 1)
        else:
            # Adds a small random value to the current weight
            self.weight += random.gauss(0, 1)/10
            if self.weight > 1:
                # Limits the weight to a maximum of 1
                self.weight = 1
            if self.weight < -1:
                # Limits the weight to a minimum of -1
                self.weight = -1

    def clone(self, from_node, to_node):
        # Creates a new instance of Connection with the same weight,
        # but different from_node and to_node values
        clone = Connection(from_node, to_node, self.weight)
        return clone
