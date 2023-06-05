from pygame import Surface, Rect
import pygame
from Button import Button


class GUI:
    """
    GUI that stores all the buttons in the form of clickable rects
    """
    color: tuple[int, int, int, int]
    rect: Rect
    buttons: list[Button]

    def __init__(self, res: tuple[int, int], color: tuple[int, int, int, int] = (128, 128, 128, 255)) -> None:
        self.color = color
        self.rect = Rect((0, 0), (res[0], 100))
        self.buttons = []

    def display(self, surface: Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)

    def construct_buttons(self) -> None:
        pass


