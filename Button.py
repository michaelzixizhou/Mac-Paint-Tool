from pygame import Surface, Rect
import pygame


class Button:
    """
    ABSTRACT

    Buttons that have a function when clicked
    """
    color: tuple[int, int, int, int]
    surface: Surface

    def __init__(self, surface: Surface, color: tuple[int, int, int, int]) -> None:
        self.color = color
        self.surface = surface

    def get_rect(self) -> Rect:
        return self.surface.get_rect()

    def onClick(self) -> None:
        raise NotImplementedError


class PenButton(Button):
    def __init__(self, surface: Surface, color: tuple[int, int, int, int]) -> None:
        super().__init__(surface, color)

    def onClick(self) -> None:
        