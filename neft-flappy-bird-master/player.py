import brain  # Importing the brain module for AI functionality
import random  # Importing the random module for generating random colors
import pygame  # Importing the pygame module for game graphics and functionality
import components # Importing the config module for accessing components configuration
import config  # Importing the config module for accessing game configuration

class Player:
    def __init__(self):
        """
        Initialize a Player object.

        Args:
            None

        Returns:
            None
        """
        # Bird
        self.x, self.y = 50, 200  # Initial position of the bird
        self.rect = pygame.Rect(self.x, self.y, 20, 20)  # Creating a rectangular shape for the bird
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)  # Random color for the bird
        self.vel = 0  # Velocity of the bird
        self.tired_lvl = 0 # Tiredness of the bird
        self.flap = False  # Flag to indicate whether the bird is flapping
        self.alive = True  # Flag to indicate whether the bird is alive
        self.lifespan = 0  # Lifespan of the bird (how long it has been alive)

        # AI
        self.decision = None  # Decision made by the AI
        self.data = [0.5, 1, 0.5, 0.5, 0, 0]  # Data input for the AI
        self.fitness = 0  # Fitness score of the bird
        self.inputs = 6  # Number of inputs for the AI
        self.brain = brain.Brain(self.inputs)  # Creating a brain for the AI
        self.brain.generate_net()  # Generating the neural network for the AI

    # Game related functions
    def draw(self, window):
        """
        Draw the bird on the game window.

        Args:
            window (pygame.Surface): The game window surface.

        Returns:
            None
        """
        pygame.draw.rect(window, self.color, self.rect)  # Drawing the bird on the game window

    def ground_collision(self, ground):
        """
        Check collision with the ground.

        Args:
            ground (pygame.Rect): The ground rectangle.

        Returns:
            bool: True if there is a collision, False otherwise.
        """
        return pygame.Rect.colliderect(self.rect, ground)  # Checking collision with the ground

    def sky_collision(self):
        """
        Check collision with the sky.

        Args:
            None

        Returns:
            bool: True if there is a collision, False otherwise.
        """
        return bool(self.rect.y < 30)  # Checking collision with the sky

    def pipe_collision(self):
        """
        Check collision with the pipes.

        Args:
            None

        Returns:
            bool: True if there is a collision, False otherwise.
        """
        for p in config.pipes:
            return pygame.Rect.colliderect(self.rect, p.top_rect) or \
                   pygame.Rect.colliderect(self.rect, p.bottom_rect)  # Checking collision with the pipes

    def update(self, ground):
        """
        Update the player's position and state.

        Args:
            ground (pygame.Rect): The ground rectangle.

        Returns:
            None
        """
        if not (self.ground_collision(ground) or self.pipe_collision()):
            # Gravity
            self.vel += 0.25  # Applying gravity to the bird
            self.rect.y += self.vel  # Updating the position of the bird based on velocity
            if self.vel > 5:
                self.vel = 5  # Limiting the maximum velocity of the bird
            if self.vel >= -1:
                self.flap = False  # Resetting the flap flag if the bird's velocity is high
            if self.vel >= -2 and not self.flap and self.tired_lvl > 0:
                self.tired_lvl -= 1
            # Increment lifespan
            self.lifespan += 1  # Incrementing the lifespan of the bird
        else:
            self.alive = False  # Marking the bird as not alive
            self.flap = False  # Resetting the flap flag
            self.vel = 0  # Resetting the velocity of the bird

    def bird_flap(self):
        """
        Make the bird flap.

        Args:
            None

        Returns:
            None
        """
        if not self.flap and not self.sky_collision():
            self.flap = True  # Setting the flap flag to True
            self.vel = -5 + self.tired_lvl  # Giving the bird an upward velocity when flapping
            if(self.tired_lvl < 2):
                self.tired_lvl += 1
        

    @staticmethod
    def closest_pipe():
        """
        Find the closest pipe.

        Args:
            None

        Returns:
            components.Pipes: The closest pipe object.
        """
        for p in config.pipes:
            if not p.passed:
                return p  # Returning the closest pipe that has not been passed yet

    # AI related functions
    def collect_data(self):
        """
        Collect data for the AI.

        Args:
            None

        Returns:
            None
        """
        self_center = self.rect.center[1]
        # If there are pipes 
        if config.pipes:
            top = self.closest_pipe().top_rect.bottom # Set the distance to the bottom of the top pipe
            bottom = self.closest_pipe().bottom_rect.top # set the x distance to the pipe
            x = self.closest_pipe().x # Set the distance to the top of the bottom pipe
            # Draw line to top pipe
            pygame.draw.line(config.window, self.color, self.rect.center,
                        (self.rect.center[0], config.pipes[0].top_rect.bottom))
            # Draw line to mid pipe
            pygame.draw.line(config.window, self.color, self.rect.center,
                        (config.pipes[0].x, self_center))
            # Draw line to bottom pipe
            pygame.draw.line(config.window, self.color, self.rect.center,
                        (self.rect.center[0], config.pipes[0].bottom_rect.top))
        # If there arent pipes
        else:
            top = config.win_height/2 - components.Pipes.opening/2 # Set the distance to the bottom of the top pipe
            x = config.win_width # set the x distance to the pipe
            bottom = config.win_height/2 + components.Pipes.opening/2 # Set the distance to the top of the bottom pipe

        self.data[0] = (self_center - top) / 500 # Calculate the distance to the bottom of the top pipe
        self.data[1] = (x - self.rect.center[0]) / 500 # Calculate the  x distance to the pipe
        self.data[2] = (bottom - self_center) / 500 # Calculate the distance to the top of the bottom pipe
        self.data[3] = (config.ground.ground_level - self_center) / 500 # Calculate the distance to the top of the bottom pipe
        self.data[4] = 1 if self.flap else 0  # If bird is flapping pass 1 to the net else pass zero
        self.data[5] = self.tired_lvl  # Pass tired_lvl to the net
        
                             
    def think(self):
        """
        Make a decision using the neural network.

        Args:
            None

        Returns:
            None
        """
        self.decision = self.brain.feed_forward(self.data)  # Making a decision using the neural network
        if self.decision > 0.63:  # Threshold for deciding to flap
            self.bird_flap()  # Flapping the bird
            
    def calculate_fitness(self):
        """
        Calculate the fitness score.

        Args:
            None

        Returns:
            None
        """
        self.fitness = self.lifespan  # Fitness is equal to the lifespan of the bird
        
    def clone(self):
        """
        Create a clone of the player.

        Args:
            None

        Returns:
            Player: A clone of the player.
        """
        clone = Player()  # Creating a clone of the bird
        clone.fitness = self.fitness  # Assigning fitness to the clone
        clone.brain = self.brain.clone()  # Cloning the brain of the bird
        clone.brain.generate_net()  # Generating the neural network for the clone
        return clone
