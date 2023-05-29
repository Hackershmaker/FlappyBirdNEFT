import pygame   # Importing the pygame library for game development
from sys import exit   # Importing the exit function from the sys module
import pandas as pd # Importing the pandas module
# Setting matplotlib to use a GUI inteface
import matplotlib # Importing matplotlib mopdule
matplotlib.use('TkAgg')  # Set the backend to TkAgg
import matplotlib.pyplot as plt # Importing the pandas module
import config   # Importing a custom module named config
import components   # Importing a custom module named components
import population   # Importing a custom module named population

pygame.init()   # Initializing the pygame library
clock = pygame.time.Clock()   # Creating a Clock object to control the frame rate of the game
population = population.Population(100)   # Creating an instance of the Population class from the population module with 100 as the initial population size

def generate_pipes():   # Defining a function named generate_pipes
    config.pipes.append(components.Pipes(config.win_width))   # Creating a Pipes object from the components module and adding it to the pipes list in the config module
    for p in config.pipes:
        if p.off_screen:
            config.pipes.remove(p)


def quit_game():   # Defining a function named quit_game
    for event in pygame.event.get():   # Iterating over the events in the event queue
        if event.type == pygame.QUIT:   # Checking if the event type is QUIT (user closed the window)
            pygame.quit()   # Quitting the pygame library
            exit()   # Exiting the program

def main():   # Defining a function named main
    max_gen = 50
    statistics_list = []
    pipes_spawn_time = 10   # Setting the initial value of pipes_spawn_time to 10

    while True:   # Entering an infinite loop
        print(f"time: {clock.get_time()}")
        quit_game()   # Calling the quit_game function to handle events and check for window close

        config.window.fill((0, 0, 0))   # Filling the window with black color

        # Spawn Ground
        config.ground.draw(config.window)   # Drawing the ground on the window

        # Spawn Pipes
        if pipes_spawn_time <= 0:   # Checking if it's time to spawn pipes
            generate_pipes()   # Calling the generate_pipes function to create new pipes
            pipes_spawn_time = 200   # Resetting the pipes_spawn_time
        pipes_spawn_time -= 1   # Decrementing the pipes_spawn_time

        for p in config.pipes:   # Iterating over the pipes in the pipes list
            p.draw(config.window)   # Drawing the pipe on the window
            p.update()   # Updating the pipe's position
            if p.off_screen:   # Checking if the pipe is off the screen
                config.pipes.remove(p)   # Removing the pipe from the pipes list

        # Move players
        if not population.extinct():   # Checking if there are still live players in the population
            population.update_live_players()   # Updating the positions of the live players
        else:
            statistics_list.append(population.get_stats())
            if not population.generation >= max_gen:
                config.pipes.clear()   # Clearing the pipes list
                population.natural_selection()   # Performing natural selection on the population
            else:
                df = pd.DataFrame.from_records(statistics_list)
                stats = {"max", "mean", "min", "75%"}
                for column_to_plot in stats:
                    plt.plot(df[column_to_plot])
                    plt.xlabel("Index")
                    plt.ylabel(f"{column_to_plot} Lifespan")
                    plt.title(f"{column_to_plot} Lifespan Distribution")
                    plt.grid(True)
                    plt.show()
                    plt.pause(0.001)
                    input("Press any key to continue...")

        clock.tick(60)   # Limiting the frame rate to 60 frames per second
        pygame.display.flip()   # Updating the contents of the entire display

main()   # Calling the main function to start the game
