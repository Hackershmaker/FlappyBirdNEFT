import random

class Connection:
    """
    Represents a connection between nodes in a neural network.

    Attributes:
        from_node: The node where the connection originates.
        to_node: The node where the connection ends.
        weight: The weight of the connection.

    Methods:
        __init__(from_node, to_node, weight):
            Initializes a new instance of the Connection class.
        mutate_weight():
            Mutates the weight of the connection.
        clone(from_node, to_node):
            Creates a clone of the Connection instance.

    """

    def __init__(self, from_node, to_node, weight):
        """
        Initializes a new instance of the Connection class.

        Args:
            from_node: The node where the connection originates.
            to_node: The node where the connection ends.
            weight: The weight of the connection.

        Returns:
            None
        """
        self.from_node = from_node  # The node where the connection originates
        self.to_node = to_node  # The node where the connection ends
        self.weight = weight  # The weight of the connection

    def mutate_weight(self):
        """
        Mutates the weight of the connection.

        The mutation process randomly assigns a completely new weight between -1 and 1
        with a 10% probability. Otherwise, a small random value is added to the current weight.
        The weight is then limited to a minimum of -1 and a maximum of 1.

        Args:
            None

        Returns:
            None
        """
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
        """
        Creates a clone of the Connection instance.

        Args:
            from_node: The node where the cloned connection originates.
            to_node: The node where the cloned connection ends.

        Returns:
            Connection: Cloned instance of the Connection class with the same weight,
                       but different from_node and to_node values.
        """
        clone = Connection(from_node, to_node, self.weight)
        return clone
