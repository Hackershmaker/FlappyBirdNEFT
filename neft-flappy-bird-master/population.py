import config  # Importing configuration settings
import player  # Importing the player module
import math  # Importing the math module for mathematical operations
import pandas as pd # Importing pandas module
import species  # Importing the species module
import operator  # Importing the operator module for sorting


class Population:
    def __init__(self, size):
        self.players = []  # List to store player objects
        self.generation = 1  # Current generation number
        self.species = []  # List to store species
        self.size = size  # Size of the population
        for i in range(0, self.size):
            self.players.append(player.Player())  # Creating player objects and adding them to the population

    def update_live_players(self):
        # Update the live players in the population
        for p in self.players:
            if p.alive:
                p.look()  # Perform player's look behavior
                p.think()  # Perform player's think behavior
                p.draw(config.window)  # Draw player on the window
                p.update(config.ground)  # Update player's position based on the ground

    def natural_selection(self):
        # Perform natural selection process
        print('SPECIATE')
        self.speciate()  # Separate players into species

        print('CALCULATE FITNESS')
        self.calculate_fitness()  # Calculate fitness for each player and species

        print('KILL EXTINCT')
        self.kill_extinct_species()  # Remove species with no players

        print('KILL STALE')
        self.kill_stale_species()  # Remove species that have not improved for a long time

        print('SORT BY FITNESS')
        self.sort_species_by_fitness()  # Sort species by fitness

        print('CHILDREN FOR NEXT GEN')
        self.next_gen()  # Generate children for the next generation

    def speciate(self):
        # Separate players into species based on similarity
        for s in self.species:
            s.players = []

        for p in self.players:
            add_to_species = False
            for s in self.species:
                if s.similarity(p.brain):  # Check if player's brain is similar to the species' representative
                    s.add_to_species(p)  # Add player to the species
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.append(species.Species(p))  # Create a new species for the player

    def calculate_fitness(self):
        # Calculate fitness for each player and species
        for p in self.players:
            p.calculate_fitness()  # Calculate fitness for individual player
        for s in self.species:
            s.calculate_average_fitness()  # Calculate average fitness for each species

    def kill_extinct_species(self):
        # Remove species with no players
        species_bin = []
        for s in self.species:
            if len(s.players) == 0:
                species_bin.append(s)
        for s in species_bin:
            self.species.remove(s)

    def kill_stale_species(self):
        # Remove species that have not improved for a long time
        player_bin = []
        species_bin = []
        for s in self.species:
            if s.staleness >= 8:
                if len(self.species) > len(species_bin) + 1:
                    species_bin.append(s)
                    for p in s.players:
                        player_bin.append(p)
                else:
                    s.staleness = 0
        for p in player_bin:
            self.players.remove(p)
        for s in species_bin:
            self.species.remove(s)

    def sort_species_by_fitness(self):
        # Sort species by fitness in descending order
        for s in self.species:
            s.sort_players_by_fitness()

        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)

    def next_gen(self):
        children = []

        # Clone champion of each species and add to children
        for s in self.species:
            children.append(s.champion.clone())

        # Fill open player slots with offspring from species
        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))
        for s in self.species:
            for i in range(0, children_per_species):
                children.append(s.offspring())

        # Add offspring from the best species until the population size is reached
        while len(children) < self.size:
            children.append(self.species[0].offspring())

        # Update the players with the new children
        self.players = []
        for child in children:
            self.players.append(child)
        self.generation += 1

    # Check if all players are dead
    def extinct(self):
        extinct = True
        for p in self.players:
            if p.alive:
                extinct = False
        return extinct
    
    def get_stats(self):
        # Create a DataFrame from the player objects
        df = pd.DataFrame([vars(player) for player in self.players])
        # Calculate statistics on the lifespan column
        lifespan_stats = df['lifespan'].describe()
        statistics_dict = lifespan_stats.to_dict()
        return statistics_dict
