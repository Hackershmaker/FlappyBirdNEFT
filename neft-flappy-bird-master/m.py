import pygame
from sys import exit
import config
import components
import population

pygame.init()
clock = pygame.time.Clock()
population = population.Population(100)

def generate_pipes():
    config.pipes.append(components.Pipes(config.win_width))

def handle_button_clicks():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            config.play_button.handle_event(event)
            config.quit_button.handle_event(event)

def draw_start_screen():
    config.window.fill((0, 0, 0))
    
    # Draw buttons
    config.play_button.draw(config.window)
    config.quit_button.draw(config.window)

def main():
    pipes_spawn_time = 10
    game_started = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if not game_started:
            handle_button_clicks()
            draw_start_screen()
        else:
            config.window.fill((0, 0, 0))

            # Spawn Ground
            config.ground.draw(config.window)

            # Spawn Pipes
            if pipes_spawn_time <= 0:
                generate_pipes()
                pipes_spawn_time = 200
            pipes_spawn_time -= 1

            for p in config.pipes:
                p.draw(config.window)
                p.update()
                if p.off_screen:
                    config.pipes.remove(p)

            # Move players
            if not population.extinct():
                population.update_live_players()
            else:
                config.pipes.clear()
                population.natural_selection()

        clock.tick(60)
        pygame.display.flip()

main()