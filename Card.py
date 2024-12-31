from CardColor import CardColor
import pygame
from pygame import Rect, Surface

class Card:
    value: int | None
    color: CardColor
    image = None
    position: int
    photo_path: str

    WIDTH = 50
    HEIGHT = 60
    GAP = 10
    Y_POSITION = 500
    STARTING_WIDTH = 50

    x_position: int = 0

    REVEAL = -1
    HIDE = -2
    BLANK_CARD_COLOR = (255, 0, 0)

    def __init__(self, value: int | None, color: CardColor, photo_path: str):
        self.value = value
        self.color = color
        self.photo_path = photo_path

        self.load_image()

    def turn_into_color_cube(self, color: CardColor, photo_path: str):
        self.photo_path = photo_path
        self.color = color
        self.load_image()

    def load_image(self):
        self.image = pygame.image.load(self.photo_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))

    def get_position(self):
        self.x_position = self.STARTING_WIDTH + (Card.WIDTH + Card.GAP) * self.position

    def draw(self, screen: Surface, reveal: REVEAL | HIDE):
        self.get_position()
        if reveal == Card.REVEAL:
            screen.blit(self.image, (self.x_position, 500))
        else:
            pygame.draw.rect(screen, self.BLANK_CARD_COLOR, pygame.Rect(self.x_position, 30, Card.WIDTH, Card.HEIGHT))

    def is_stop(self):
        return 'stop' in self.photo_path

    def is_color_changer(self):
        return 'color_changer' in self.photo_path

    def is_change_direction(self):
        return 'change_direction' in self.photo_path

    def is_plus_two(self):
        return 'plus_two' in self.photo_path

    def is_number(self):
        return self.value is not None

    def is_taki(self):
        return 'taki' in self.photo_path

    def display_string(self):
        color = CardColor(self.color).name

        if self.is_stop():
            return f"{color} STOP"
        elif self.is_color_changer():
            return 'Color Changer' if color == 'White' else f"{color} Color Changer"
        elif self.is_change_direction():
            return f"{color} Change Direction"
        elif self.is_plus_two():
            return f"{color} +2"
        elif self.is_number():
            return f"{color} {self.value}"
        elif self.is_taki():
            return f"{color} Taki"