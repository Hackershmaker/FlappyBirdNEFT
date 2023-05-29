import operator
import random

class Species:
    def __init__(self, player):
        # Initialize a new species with a player
        self.players = []  # List to store players belonging to this species
        self.average_fitness = 0  # Average fitness of players in this species
        self.threshold = 1.2  # Similarity threshold for determining if a brain is in the same species
        self.players.append(player)  # Add the initial player to the species
        self.benchmark_fitness = player.fitness  # The highest fitness achieved by any player in this species
        self.benchmark_brain = player.brain.clone()  # The brain of the player with the highest fitness
        self.champion = player.clone()  # The player with the highest fitness
        self.staleness = 0  # Number of generations since the fitness of the champion improved

    def similarity(self, brain):
        # Calculate the similarity between the given brain and the benchmark brain of this species
        similarity = self.weight_difference(self.benchmark_brain, brain)
        return self.threshold > similarity

    @staticmethod
    def weight_difference(brain_1, brain_2):
        # Calculate the total weight difference between two brains
        total_weight_difference = 0
        for i in range(0, len(brain_1.connections)):
            for j in range(0, len(brain_2.connections)):
                if i == j:
                    total_weight_difference += abs(brain_1.connections[i].weight - brain_2.connections[j].weight)
        return total_weight_difference

    def add_to_species(self, player):
        # Add a player to this species
        self.players.append(player)

    def sort_players_by_fitness(self):
        # Sort the players in this species by their fitness in descending order
        self.players.sort(key=operator.attrgetter('fitness'), reverse=True)
        if self.players[0].fitness > self.benchmark_fitness:
            # If the highest fitness improved, update the benchmark and champion
            self.staleness = 0
            self.benchmark_fitness = self.players[0].fitness
            self.champion = self.players[0].clone()
        else:
            # Otherwise, increment the staleness counter
            self.staleness += 1

    def calculate_average_fitness(self):
        # Calculate the average fitness of players in this species
        total_fitness = 0
        for p in self.players:
            total_fitness += p.fitness
        if self.players:
            self.average_fitness = int(total_fitness / len(self.players))
        else:
            self.average_fitness = 0

    def offspring(self):
        # Create an offspring by randomly selecting a player from this species and mutating its brain
        baby = self.players[random.randint(1, len(self.players)) - 1].clone()
        baby.brain.mutate()
        return baby
