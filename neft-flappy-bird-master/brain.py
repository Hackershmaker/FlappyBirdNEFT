import node
import connection
import random

class Brain:
    """
    Represents a neural network.

    Attributes:
        connections (list): List of connections between nodes.
        nodes (list): List of nodes in the network.
        inputs (int): Number of input nodes in the network.
        net (list): Ordered list of nodes representing the network.
        layers (int): Number of layers in the network.

    Methods:
        __init__(inputs, clone=False):
            Initializes a new instance of the Brain class.
        connect_nodes():
            Connects the nodes in the network.
        generate_net():
            Generates the network based on node layers.
        feed_forward(data):
            Performs a feed-forward operation on the network.
        clone():
            Creates a clone of the Brain instance.
        getNode(id):
            Returns the node with the specified ID.
        mutate():
            Applies mutation to the connections of the network.
    """

    def __init__(self, inputs, clone=False): 
        """
        Initializes a new instance of the Brain class.

        Args:
            inputs (int): Number of input nodes in the network.
            clone (bool, optional): Indicates if this is a clone of another Brain instance.

        Returns:
            None
        """
        self.connections = []  # List to store connections between nodes
        self.nodes = []  # List to store nodes in the network
        self.inputs = inputs  # Number of input nodes in the network
        self.net = []  # Ordered list of nodes representing the network
        self.layers = 2  # Number of layers in the network

        if not clone:
            # Create input nodes
            for i in range(0, self.inputs):
                self.nodes.append(node.Node(i))  # Create a new node
                self.nodes[i].layer = 0  # Set the layer of the node as 0 (input layer)
            # Create bias node
            self.nodes.append(node.Node(6))  # Create a new node with ID 6
            self.nodes[6].layer = 0  # Set the layer of the bias node as 0 (input layer)
            # Create output node
            self.nodes.append(node.Node(7))  # Create a new node with ID 7
            self.nodes[7].layer = 1  # Set the layer of the output node as 1 (output layer)

            # Create connections
            for i in range(0, 7):
                self.connections.append(connection.Connection(self.nodes[i], self.nodes[7], random.uniform(-1, 1)))
                # Create a new connection with a random weight between -1 and 1

    def connect_nodes(self):
        """
        Connects the nodes in the network.

        Args:
            None

        Returns:
            None
        """
        for i in range(0, len(self.nodes)):
            self.nodes[i].connections = []  # Clear the connections list of each node

        for i in range(0, len(self.connections)):
            self.connections[i].from_node.connections.append(self.connections[i])
            # Add the connection to the from_node's connections list

    def generate_net(self):
        """
        Generates the network based on node layers.

        Args:
            None

        Returns:
            None
        """
        self.connect_nodes()  # Connect the nodes in the network
        self.net = []  # Clear the net list

        for j in range(0, self.layers):
            for i in range(0, len(self.nodes)):
                if self.nodes[i].layer == j:
                    self.net.append(self.nodes[i])
                    # Add the node to the net list if it belongs to the current layer

    def feed_forward(self, data):
        """
        Performs a feed-forward operation on the network.

        Args:
            data (list): Input data for the network.

        Returns:
            float: Output value of the network.
        """
        for i in range(0, self.inputs):
            self.nodes[i].output_value = data[i]
            # Set the output values of input nodes based on the given data

        self.nodes[6].output_value = 1  # Set the output value of the bias node to 1

        for i in range(0, len(self.net)):
            self.net[i].activate()
            # Activate the nodes in the network

        output_value = self.nodes[7].output_value  # Get output value from the output node

        for i in range(0, len(self.nodes)):
            self.nodes[i].input_value = 0
            # Reset the input values of all nodes

        return output_value

    def clone(self):
        """
        Creates a clone of the Brain instance.

        Args:
            None

        Returns:
            Brain: Cloned Brain instance.
        """
        clone = Brain(self.inputs, True)  # Create a new Brain instance with the same input count

        for n in self.nodes:
            clone.nodes.append(n.clone())  # Clone all the nodes from the current instance

        for c in self.connections:
            clone.connections.append(c.clone(clone.getNode(c.from_node.id), clone.getNode(c.to_node.id)))
            # Clone all the connections from the current instance, using the cloned nodes

        clone.layers = self.layers  # Set the layer count of the cloned instance
        clone.connect_nodes()  # Connect the nodes in the cloned instance

        return clone

    def getNode(self, id):
        """
        Returns the node with the specified ID.

        Args:
            id (int): ID of the desired node.

        Returns:
            Node: The node with the specified ID.
        """
        for n in self.nodes:
            if n.id == id:
                return n  # Return the node with the given ID

    def mutate(self):
        """
        Applies mutation to the connections of the network.

        Args:
            None

        Returns:
            None
        """
        if random.uniform(0, 1) < 0.8:
            # There is an 80% chance that a connection undergoes mutation
            for i in range(0, len(self.connections)):
                self.connections[i].mutate_weight()
                # Mutate the weights of the connections with an 80% chance
