import brain  # Importing the brain module for AI functionality
import random  # Importing the random module for generating random colors
import pygame  # Importing the pygame module for game graphics and functionality
import config  # Importing the config module for accessing game configuration

class Player:
    def __init__(self):
        # Bird
        self.x, self.y = 50, 200  # Initial position of the bird
        self.rect = pygame.Rect(self.x, self.y, 20, 20)  # Creating a rectangular shape for the bird
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)  # Random color for the bird
        self.vel = 0  # Velocity of the bird
        self.flap = False  # Flag to indicate whether the bird is flapping
        self.alive = True  # Flag to indicate whether the bird is alive
        self.lifespan = 0  # Lifespan of the bird (how long it has been alive)

        # AI
        self.decision = None  # Decision made by the AI
        self.vision = [0.5, 1, 0.5]  # Vision input for the AI
        self.fitness = 0  # Fitness score of the bird
        self.inputs = 3  # Number of inputs for the AI
        self.brain = brain.Brain(self.inputs)  # Creating a brain for the AI
        self.brain.generate_net()  # Generating the neural network for the AI

    # Game related functions
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)  # Drawing the bird on the game window

    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)  # Checking collision with the ground

    def sky_collision(self):
        return bool(self.rect.y < 30)  # Checking collision with the sky

    def pipe_collision(self):
        for p in config.pipes:
            return pygame.Rect.colliderect(self.rect, p.top_rect) or \
                   pygame.Rect.colliderect(self.rect, p.bottom_rect)  # Checking collision with the pipes

    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision()):
            # Gravity
            self.vel += 0.25  # Applying gravity to the bird
            self.rect.y += self.vel  # Updating the position of the bird based on velocity
            if self.vel > 5:
                self.vel = 5  # Limiting the maximum velocity of the bird
            # Increment lifespan
            self.lifespan += 1  # Incrementing the lifespan of the bird
        else:
            self.alive = False  # Marking the bird as not alive
            self.flap = False  # Resetting the flap flag
            self.vel = 0  # Resetting the velocity of the bird

    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.flap = True  # Setting the flap flag to True
            self.vel = -5  # Giving the bird an upward velocity when flapping
        if self.vel >= -1:
            self.flap = False  # Resetting the flap flag if the bird's velocity is high

    @staticmethod
    def closest_pipe():
        for p in config.pipes:
            if not p.passed:
                return p  # Returning the closest pipe that has not been passed yet

    # AI related functions
    def look(self):
        if config.pipes:
            # Line to top pipe
            self.vision[0] = max(0, self.rect.center[1] - self.closest_pipe().top_rect.bottom) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].top_rect.bottom))
            
            # Line to mid pipe
            self.vision[1] = max(0, self.closest_pipe().x - self.rect.center[0]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (config.pipes[0].x, self.rect.center[1]))
            
            # Line to bottom pipe
            self.vision[2] = max(0, self.closest_pipe().bottom_rect.top - self.rect.center[1]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].bottom_rect.top))
                             
    def think(self):
        self.decision = self.brain.feed_forward(self.vision)  # Making a decision using the neural network
        if self.decision > 0.73:  # Threshold for deciding to flap
            self.bird_flap()  # Flapping the bird
            
    def calculate_fitness(self):
        self.fitness = self.lifespan  # Fitness is equal to the lifespan of the bird
        
    def clone(self):
        clone = Player()  # Creating a clone of the bird
        clone.fitness = self.fitness  # Assigning fitness to the clone
        clone.brain = self.brain.clone()  # Cloning the brain of the bird
        clone.brain.generate_net()  # Generating the neural network for the clone
        return clone
