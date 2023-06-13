from pygame import Surface, Rect
import pygame
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

    def onClick(self) -> int:
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

    def onClick(self) -> int:
        raise NotImplementedError

    def display(self, surface: Surface) -> None:
        super().display(surface)
        surface.blit(self.icon, self.rect)

class PenButton(IconButton):
    icon: Surface
    def __init__(self, rect: Rect, color: Union[tuple[int, int, int, int], pygame.Color], icon: Surface) -> None:
        super().__init__(rect, color, icon)

    def onClick(self) -> int:
        print("drawing")        
        return 1

class EraserButton(IconButton):
    def __init__(self, rect: Rect, color: Union[tuple[int, int, int, int], pygame.Color], icon: Surface) -> None:
        super().__init__(rect, color, icon)

    def onClick(self) -> int:
        print("eraser")
        return 2

class MovementButton(IconButton):
    def __init__(self, rect: Rect, color: Union[tuple[int, int, int, int], pygame.Color], icon: Surface) -> None:
        super().__init__(rect, color, icon)

    def onClick(self) -> int:
        print("movement")
        return 3

class ClearButton(IconButton):
    def __init__(self, rect: Rect, color: Union[tuple[int, int, int, int], pygame.Color], icon: Surface) -> None:
        super().__init__(rect, color, icon)

    def onClick(self) -> int:
        print("clearing board")
        return 4

class TextButton(IconButton):
    def __init__(self, rect: Rect, color: Union[tuple[int, int, int, int], pygame.Color], icon: Surface) -> None:
        super().__init__(rect, color, icon)

    def onClick(self) -> int:
        print("text")
        return 5

class TextColorButton(Button):
    def __init__(self, rect: Rect, color: Union[tuple[int, int, int, int], pygame.Color]) -> None:
        super().__init__(rect, color)
    
    def onClick(self) -> int:
        return 6

class TextApplyButton(IconButton):
    def __init__(self, rect: Rect, color: Union[tuple[int, int, int, int], pygame.Color], icon: Surface) -> None:
        super().__init__(rect, color, icon)

    def onClick(self) -> int:
        return 7
