import pygame
import random

class Ground:
    ground_level = 500

    def __init__(self, win_width):
        # Initialize the Ground object with its position and dimensions
        self.x, self.y = 0, Ground.ground_level
        self.rect = pygame.Rect(self.x, self.y, win_width, 5)

    def draw(self, window):
        # Draw the ground on the window
        pygame.draw.rect(window, (255, 255, 255), self.rect)

class Pipes:
    width = 15
    opening = 100

    def __init__(self, win_width):
        # Initialize the Pipes object with its position, dimensions, and flags
        self.x = win_width
        self.bottom_height = random.randint(10, 300)
        self.top_height = Ground.ground_level - self.bottom_height - self.opening
        self.bottom_rect, self.top_rect = pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)
        self.passed = False
        self.off_screen = False

    def draw(self, window):
        # Draw the bottom and top pipes on the window
        self.bottom_rect = pygame.Rect(self.x, Ground.ground_level - self.bottom_height, self.width, self.bottom_height)
        pygame.draw.rect(window, (255, 255, 255), self.bottom_rect)

        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        pygame.draw.rect(window, (255, 255, 255), self.top_rect)

    def update(self):
        # Update the position of the pipes
        self.x -= 1
        if self.x + Pipes.width <= 50:
            self.passed = True
        if self.x <= -self.width:
            self.off_screen = True

class Button:
    def __init__(self, x, y, width, height, text, text_color, button_color, font_size, action):
        # Initialize the Button object with its position, dimensions, and attributes
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.font_size = font_size
        self.action = action

    def draw(self, surface):
        # Draw the button on the given surface
        pygame.draw.rect(surface, self.button_color, self.rect)
        font = pygame.font.Font(None, self.font_size)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def handle_event(self, event):
        # Handle the event triggered by the button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()