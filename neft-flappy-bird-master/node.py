import math

class Node:
    def __init__(self, id_number):
        """
        Initialize a Node object with an ID number.

        Args:
            id_number (int): The ID number of the node.

        Returns:
            None
        """
        self.id = id_number
        self.layer = 0  # Initialize layer as 0
        self.input_value = 0  # Initialize input value as 0
        self.output_value = 0  # Initialize output value as 0
        self.connections = []  # Create an empty list to store connections

    def activate(self):
        """
        Activate the node by applying the sigmoid activation function to the input value.

        Args:
            None

        Returns:
            None
        """
        def sigmoid(x):  # Define a sigmoid activation function
            """
            Compute the sigmoid function.

            Args:
                x (float): Input value.

            Returns:
                float: Result of the sigmoid function.
            """
            return 1 / (1 + math.exp(-x))

        if self.layer == 1:  # Check if the node is in layer 1
            self.output_value = sigmoid(self.input_value)  # Apply sigmoid activation to the input value

        for i in range(0, len(self.connections)):  # Iterate over the connections
            self.connections[i].to_node.input_value += \
                self.connections[i].weight * self.output_value  # Add the weighted output value to the connected node's input value

    def clone(self):
        """
        Create a clone of the node with the same ID and layer.

        Args:
            None

        Returns:
            Node: A clone of the node.
        """
        clone = Node(self.id)  # Create a new instance of Node with the same ID
        clone.id = self.id  # Set the ID of the clone to the ID of the original node
        clone.layer = self.layer  # Set the layer of the clone to the layer of the original node
        return clone  # Return the clone instance
