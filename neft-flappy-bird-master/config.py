import components       # Importing the components module
import pygame           # Importing the pygame module

# Initialize display
win_height = 720         # Setting the height of the game window
win_width = 550          # Setting the width of the game window
window = pygame.display.set_mode((win_width, win_height))   # Creating the game window with the specified dimensions
pygame.display.set_caption('Flappy Bird')   # Setting the caption of the game window

# Initialize pygame font
pygame.font.init()   # Initializing the pygame font module
font = pygame.font.Font(None, 36)   # Creating a font object with a font size of 36

# Create components
play_button = components.Button(100, 200, 200, 50, "Play", (0, 0, 0), (255, 255, 255), 36, lambda: start_game())
# Creating a button object for the play button with specified dimensions, text, colors, and font size, and a lambda function that calls the start_game() function
quit_button = components.Button(100, 300, 200, 50, "Quit", (0, 0, 0), (255, 255, 255), 36, lambda: quit_game())
# Creating a button object for the quit button with specified dimensions, text, colors, and font size, and a lambda function that calls the quit_game() function
ground = components.Ground(win_width)   # Creating a ground object with the specified width
pipes = []   # Creating an empty list to store the pipe objects

def quit_game():
    pygame.quit()   # Quitting the pygame module
    exit()   # Exiting the program

def start_game():
    global game_started   # Declaring the variable as global to modify it inside the function
    game_started = True   # Setting the game_started variable to True, indicating that the game has started
