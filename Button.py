from pygame import Surface, Rect
import pygame
from Clipboard import Clipboard


class Button():
    """
    ABSTRACT

    Buttons that have a function when clicked
    """
    color: tuple[int, int, int, int]
    rect: Rect

    def __init__(self, rect: Rect, color: tuple[int, int, int, int]) -> None:
        self.color = color
        self.rect = rect

    def __repr__(self) -> str:
        return str(type(self))

    def get_rect(self) -> Rect:
        return self.rect

    def onClick(self, clipboard: Clipboard) -> None:
        raise NotImplementedError


class PenButton(Button):
    def __init__(self, rect: Rect, color: tuple[int, int, int, int]) -> None:
        super().__init__(rect, color)

    def onClick(self, clipboard: Clipboard) -> None:
        print("drawing")        
        clipboard.mode = "drawing"


class EraserButton(Button):
    def __init__(self, rect: Rect, color: tuple[int, int, int, int]) -> None:
        super().__init__(rect, color)

    def onClick(self, clipboard: Clipboard) -> None:
        print("eraser")
        clipboard.mode = "eraser"


class MovementButton(Button):
    def __init__(self, rect: Rect, color: tuple[int, int, int, int]) -> None:
        super().__init__(rect, color)

    def onClick(self, clipboard: Clipboard) -> None:
        print("movement")
        clipboard.mode = "movement"


class ClearButton(Button):
    def __init__(self, rect: Rect, color: tuple[int, int, int, int]) -> None:
        super().__init__(rect, color)

    def onClick(self, clipboard: Clipboard) -> None:
        print("clearing board")
        clipboard.drawBoard.clearBoard()


class TextButton(Button):
    def __init__(self, rect: Rect, color: tuple[int, int, int, int]) -> None:
        super().__init__(rect, color)
    
    def onClick(self, clipboard: Clipboard) -> None:
        clipboard.mode = "text"