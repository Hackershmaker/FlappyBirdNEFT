import components       # Importing the components module
import pygame           # Importing the pygame module
import os               # Importing the os module

# Initialize display
win_height = 720         # Setting the height of the game window
win_width = 550          # Setting the width of the game window
window = pygame.display.set_mode((win_width, win_height))   # Creating the game window with the specified dimensions
pygame.display.set_caption('Flappy Bird')   # Setting the caption of the game window

# Initialize pygame font
pygame.font.init()   # Initializing the pygame font module
font = pygame.font.SysFont("arialblack", 36)   # Creating a font object with a font size of 36

# Define coloes
TEXT_COL = (255, 255, 255)
BBACKGROUND_COL = (0, 0, 0)

# Create components
# Create buttons
play_button = components.Button(win_width/2 - 80, win_height/5 - 20, font, "Play") # Creating a button object for the play button 
quit_button = components.Button(win_width/2 - 80, win_height/5 + 30, font, "Quit") # Creating a button object for the quit button
statistics_button = components.Button(win_width/2 - 80, win_height/5 + 80, font, "Statistics") # Creating a button object for the play button 

ground = components.Ground(win_width)   # Creating a ground object with the specified width
pipes = []   # Creating an empty list to store the pipe objects

def load_stats_image():
    # Load image and resize it
    # New size
    new_width = 250
    new_height = 250
    stats_image_path = os.path.join(f'{os.getcwd()}', "max.png") # Get image path
    stats_image = pygame.image.load(stats_image_path) # Load image
    resized_image = pygame.transform.scale(stats_image, (new_width, new_height)) # Resize image
    return resized_image