import pygame   # Importing the pygame library for game development
from sys import exit   # Importing the exit function from the sys module]
import pandas as pd # Importing the pandas module
# Setting matplotlib to use a GUI inteface
import matplotlib # Importing matplotlib mopdule
matplotlib.use('Agg')  # Set the backend to TkAgg
import matplotlib.pyplot as plt # Importing the pandas module
import config   # Importing a custom module named config
import components   # Importing a custom module named components
import population   # Importing a custom module named population

pygame.init()   # Initializing the pygame library
clock = pygame.time.Clock()   # Creating a Clock object to control the frame rate of the game
population = population.Population(100)   # Creating an instance of the Population class from the population module with 100 as the initial population size

# Game variables
start_flag = True # Defining a flag to see if the game was just launched and initializing it to True
paused_flag = False # Defining a flag to see if we are in a menu and initializing it to False
click_flag = False # Defining a flag to see if the mouse was clicked
display_stats = False # Defining a flag to see if the stats should be displayed and setting it to false

def generate_pipes():   # Defining a function to generate_pipes
    """
    Generate new pipes and remove off-screen pipes.

    Args:
        None

    Returns:
        None
    """
    config.pipes.append(components.Pipes(config.win_width))   # Creating a Pipes object from the components module and adding it to the pipes list in the config module
    for p in config.pipes: # Removing pipes if off screen
        if p.off_screen:
            config.pipes.remove(p)

def event_handeler():   # Defining a function to handle events
    """
    Handel all events 

    Args:
        None

    Returns:
        None
    """
    for event in pygame.event.get():   # Iterating over the events in the event queue
        if event.type == pygame.QUIT:   # Checking if the event type is QUIT (user closed the window)
            pygame.quit()   # Quitting the pygame library
            exit()   # Exiting the program
        # Check paused
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                global paused_flag 
                paused_flag = True
                global display_stats
                display_stats = False # Reset display stats flag so stas arent displayed automatily
        # Check mouse press
        if event.type == pygame.MOUSEBUTTONUP:
            global click_flag
            click_flag = True # Set click_flack to True to indicate mouse press

def draw_text(text, font, text_col, x, y): # Defining a function to draw_text
    img = font.render(text, True, text_col)
    config.window.blit(img, (x, y))

def save_stats(statistics_list): # Defining a function to handle saving the statistic data
    df = pd.DataFrame.from_records(statistics_list) # Create a data frame from the data
    stats = {"max", "mean", "min", "75%"}
    for column_to_plot in stats:
        plt.clf() # Clear the plot
        plt.plot(df[column_to_plot]) # Convert pandas data frame to plot
        plt.xlabel("Index") # Lable x axis
        plt.ylabel(f"{column_to_plot} Lifespan") # Lable y axis
        plt.title(f"{column_to_plot} Lifespan Distribution") # Title plot
        plt.grid(True)
        plt.savefig(f'{column_to_plot}.png')  # Save the plot

def main():   # Defining a function named main
    """
    Main game loop.

    Args:
        None

    Returns:
        None
    """
    max_gen = 100 # defining the max gen
    max_pipes_passed = 100 # defining the max amount of pipes(could also be thought as the amount of pipes to win the game) 
    statistics_list = [] # Initializing a list for stats
    pipes_spawn_time = 10 # Setting the initial value of pipes_spawn_time to 10
    pipes_passed = 0 # Count of passed pipes
    global display_stats # Accessing display_stats
    global paused_flag # Accessing paused_flag
    global start_flag # Accessing start_flag
    global click_flag # Accessing click_flag

    while True:   # Entering the game loop, the loop is infinate
        if click_flag:
            click_flag = False
        event_handeler()   # Calling the quit_game function to handle events and check for window close
        # Check if the game just started
        if start_flag: # Game just started
            # Display start menu
            if config.play_button.draw(config.window, click_flag): # Displaying play button
                start_flag = False
            if config.quit_button.draw(config.window, click_flag): # Displaying quit button
                pygame.quit()   # Quitting the pygame library
                exit()   # Exiting the program
            draw_text('you can pause the game(training proccess)', config.font, config.TEXT_COL, 10, config.win_height/2) # Displaying pause game instractions            
            draw_text('at any time by precing ESC', config.font, config.TEXT_COL, 10, config.win_height/2 + 50) # Displaying pause game instractions
        else: # Game hasnt just started
            # Check if the game is paused                 
            if paused_flag: # Game is paused
                # Display menu
                config.window.fill((0, 0, 0))   # Filling the window with black color
                if config.play_button.draw(config.window, click_flag): # Displaying play button
                    paused_flag = False
                if config.quit_button.draw(config.window, click_flag): # Displaying quit button
                    pygame.quit()   # Quitting the pygame library
                    exit()   # Exiting the program
                if population.generation > 1: # Display statistics button only if ther are statistics to display
                    save_stats(statistics_list)
                    if config.statistics_button.draw(config.window, click_flag): # Displaying statistics button
                        display_stats = not display_stats
                        stats_image = config.load_stats_image()
                if display_stats: # Check if stats should be displayed and display them
                    config.window.blit(stats_image, (config.win_width/2 - 125, 276)) # Display stats

            else: # Game isnt paused
                config.window.fill((0, 0, 0))   # Filling the window with black color

                # Spawn Ground
                config.ground.draw(config.window)   # Drawing the ground on the window

                # Spawn Pipes
                if pipes_spawn_time <= 0:   # Checking if it's time to spawn pipes
                    generate_pipes()   # Calling the generate_pipes function to create new pipes
                    pipes_spawn_time = 200   # Resetting the pipes_spawn_time
                pipes_spawn_time -= 1   # Decrementing the pipes_spawn_time

                for p in config.pipes:   # Iterating over the pipes in the pipes list
                    if p.passed == True and p.counted == False: # Check if pipe was passed and counted
                        p.counted = True # If not passed set counted to true
                        pipes_passed += 1  # Increment the pipe count                      
                    p.draw(config.window)   # Drawing the pipe on the window
                    p.update()   # Updating the pipe's position
                    if p.off_screen:   # Checking if the pipe is off the screen
                        config.pipes.remove(p)   # Removing the pipe from the pipes list

                # Display number of gen and pipes passed
                draw_text(f'Gen: {population.generation}', config.font, config.TEXT_COL, 10, 600)
                draw_text(f'Pipes: {pipes_passed}', config.font, config.TEXT_COL, 10, 640)
                
                # Move players
                if not population.extinct() and not population.generation >= max_gen and not pipes_passed >= max_pipes_passed:   # Checking if there are still live players in the population and if the the stop conditions havnt been met
                    population.update_live_players()   # Updating the positions of the live players
                else:
                    statistics_list.append(population.get_stats())
                    if not population.generation >= max_gen and not pipes_passed >= max_pipes_passed:
                        config.pipes.clear()   # Clearing the pipes list
                        pipes_passed = 0 # Reset the pipe count
                        population.natural_selection()   # Performing natural selection on the population\
                    else:
                        save_stats(statistics_list)
                        pygame.quit()   # Quitting the pygame library
                        exit()   # Exiting the program


        clock.tick(60)   # Limiting the frame rate to 60 frames per second
        pygame.display.flip()   # Updating the contents of the entire display

main()   # Calling the main function to start the game
