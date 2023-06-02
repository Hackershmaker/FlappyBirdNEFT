import pygame
import random

class Ground:
    """
    Represents the ground in the game.

    Attributes:
        ground_level (int): The y-coordinate of the ground level.

    Methods:
        __init__(win_width):
            Initializes a new instance of the Ground class.
        draw(window):
            Draws the ground on the window.
    """
    ground_level = 500

    def __init__(self, win_width):
        """
        Initializes a new instance of the Ground class.

        Args:
            win_width (int): The width of the game window.

        Returns:
            None
        """
        # Initialize the Ground object with its position and dimensions
        self.x, self.y = 0, Ground.ground_level
        self.rect = pygame.Rect(self.x, self.y, win_width, 5)

    def draw(self, window):
        """
        Draws the ground on the window.

        Args:
            window (pygame.Surface): The game window surface to draw on.

        Returns:
            None
        """
        # Draw the ground on the window
        pygame.draw.rect(window, (255, 255, 255), self.rect)

class Pipes:
    """
    Represents the pipes in the game.

    Attributes:
        width (int): The width of the pipes.
        opening (int): The vertical space between the top and bottom pipes.

    Methods:
        __init__(win_width):
            Initializes a new instance of the Pipes class.
        draw(window):
            Draws the bottom and top pipes on the window.
        update():
            Updates the position of the pipes.
    """
    width = 15
    opening = 100

    def __init__(self, win_width):
        """
        Initializes a new instance of the Pipes class.

        Args:
            win_width (int): The width of the game window.

        Returns:
            None
        """
        # Initialize the Pipes object with its position, dimensions, and flags
        self.x = win_width
        self.bottom_height = random.randint(10, 300)
        self.top_height = Ground.ground_level - self.bottom_height - self.opening
        self.bottom_rect, self.top_rect = pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)
        self.passed = False
        self.off_screen = False
        self.counted = False

    def draw(self, window):
        """
        Draws the bottom and top pipes on the window.

        Args:
            window (pygame.Surface): The game window surface to draw on.

        Returns:
            None
        """
        # Draw the bottom and top pipes on the window
        self.bottom_rect = pygame.Rect(self.x, Ground.ground_level - self.bottom_height, self.width, self.bottom_height)
        pygame.draw.rect(window, (255, 255, 255), self.bottom_rect)

        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        pygame.draw.rect(window, (255, 255, 255), self.top_rect)

    def update(self):
        """
        Updates the position of the pipes.

        Args:
            None

        Returns:
            None
        """
        # Update the position of the pipes
        self.x -= 1
        if self.x + Pipes.width <= 50:
            self.passed = True
        if self.x <= -self.width:
            self.off_screen = True

class Button:
    """
    Represents a button in the game.

    Attributes:
        rect (pygame.Rect): The rectangular object representing the button.
        clicked (bool): Indicates if the button has been clicked.
        text (str): The text displayed on the button.
        font (pygame.font.Font): The font used for the button text.

    Methods:
        __init__(x, y, text='', width=160, height=40, scale=1):
            Initializes a new instance of the Button class.
        draw(surface):
            Draws the button on the given surface and handles click events.
    """

    def __init__(self, x, y, font, text = '', width = 160, height = 40, scale = 1):
        """
    Initializes a new instance of the Button class.

    Args:
        x (int): The x-coordinate of the button.
        y (int): The y-coordinate of the button.
        text (str): The text displayed on the button (default: '').
        width (int): The width of the button (default: 160).
        height (int): The height of the button (default: 40).
        scale (int): The scaling factor for the button dimensions (default: 1).

    Returns:
        None
    """
        self.rect = pygame.Rect(x, y, width * scale, height * scale) # Create a rectangular object to represent the button
        self.clicked = False # Initialize the clicked state of the button
        self.text = text # Set the text to be displayed on the button
        self.font = font # Set the font used for the button text

    def draw(self, surface, click_flag):
        """
        Draws the button on the given surface and handles click events.

        Args:
            surface (pygame.Surface): The surface on which to draw the button.

        Returns:
            bool: Indicates if the button was clicked.
        """
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos) and click_flag:
            action = True

        # draw button on screen
        pygame.draw.rect(surface, (128, 128, 128), self.rect)

        # draw text on button
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

        return action
