from pygame import Surface, Rect
import pygame
from Clipboard import Clipboard
from typing import Union, Optional


class Button():
    """
    ABSTRACT

    Buttons that have a function when clicked
    """
    color: Union[tuple[int, int, int, int], pygame.Color]
    rect: Rect

    def __init__(self, rect: Rect, color: Union[tuple[int, int, int, int], pygame.Color]) -> None:
        self.color = color
        self.rect = rect

    def __repr__(self) -> str:
        return str(type(self))

    def get_rect(self) -> Rect:
        return self.rect

    def onClick(self, clipboard: Clipboard) -> None:
        raise NotImplementedError
    
    def display(self, surface: Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)

class IconButton(Button):
    """
    ABSTRACT
    """
    icon: Surface
    def __init__(self, rect: Rect, color: Union[tuple[int, int, int, int], pygame.Color], icon: Surface) -> None:
        super().__init__(rect, color)
        self.icon = pygame.transform.scale(icon, (self.rect.w, self.rect.h))

    def onClick(self, clipboard: Clipboard) -> None:
        raise NotImplementedError

    def display(self, surface: Surface) -> None:
        super().display(surface)
        surface.blit(self.icon, self.rect)

class PenButton(IconButton):
    icon: Surface
    def __init__(self, rect: Rect, color: Union[tuple[int, int, int, int], pygame.Color], icon: Surface) -> None:
        super().__init__(rect, color, icon)

    def onClick(self, clipboard: Clipboard) -> None:
        print("drawing")        
        clipboard.mode = "drawing"

class EraserButton(IconButton):
    def __init__(self, rect: Rect, color: Union[tuple[int, int, int, int], pygame.Color], icon: Surface) -> None:
        super().__init__(rect, color, icon)

    def onClick(self, clipboard: Clipboard) -> None:
        print("eraser")
        clipboard.mode = "eraser"

class MovementButton(IconButton):
    def __init__(self, rect: Rect, color: Union[tuple[int, int, int, int], pygame.Color], icon: Surface) -> None:
        super().__init__(rect, color, icon)

    def onClick(self, clipboard: Clipboard) -> None:
        print("movement")
        clipboard.mode = "movement"

class ClearButton(IconButton):
    def __init__(self, rect: Rect, color: Union[tuple[int, int, int, int], pygame.Color], icon: Surface) -> None:
        super().__init__(rect, color, icon)

    def onClick(self, clipboard: Clipboard) -> None:
        print("clearing board")
        clipboard.drawBoard.clearBoard()
        clipboard.boxes = []

class TextButton(IconButton):
    def __init__(self, rect: Rect, color: Union[tuple[int, int, int, int], pygame.Color], icon: Surface) -> None:
        super().__init__(rect, color, icon)

    def onClick(self, clipboard: Clipboard) -> None:
        print("text")
        clipboard.mode = "text"

class TextColorButton(Button):
    def __init__(self, rect: Rect, color: Union[tuple[int, int, int, int], pygame.Color]) -> None:
        super().__init__(rect, color)
    
    def onClick(self, clipboard: Clipboard) -> None:
        self.color = clipboard.gui.palette.get_color()

class TextApplyButton(IconButton):
    def __init__(self, rect: Rect, color: Union[tuple[int, int, int, int], pygame.Color], icon: Surface) -> None:
        super().__init__(rect, color, icon)

    def onClick(self, clipboard: Clipboard) -> None:
        clipboard.moving = True
        clipboard.eraser_check = True
