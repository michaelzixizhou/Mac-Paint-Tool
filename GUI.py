from pygame import Surface, Rect
import pygame
import Button
from Clipboard import Clipboard


class GUI():
    """
    GUI that stores all the buttons in the form of clickable rects
    """
    clipboard: Clipboard
    color: tuple[int, int, int, int]
    rect: Rect
    buttons: list[Button.Button]
    screen: Surface

    def __init__(self, cb: Clipboard, res: tuple[int, int], screen: Surface, color: tuple[int, int, int, int] = (128, 128, 128, 255), \
                 width: int = 50, buttonspacing: int = 5) -> None:
        self.clipboard = cb
        self.color = color
        self.width = width
        self.rect = Rect((0, 0), (res[0], width))
        self.buttons = []
        self.screen = screen

        self.buttonspacing = buttonspacing
        self.buttonpos = buttonspacing
        self.buttonsize = width - 2 * buttonspacing

        self.construct_buttons()

    def display(self, surface: Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)

        for button in self.buttons:
            pygame.draw.rect(self.clipboard.screen, button.color, button.rect)

    def check_collision(self, event: pygame.event.Event, clipboard: Clipboard) -> None:
        for button in self.buttons:
            if button.get_rect().collidepoint(event.pos):
                button.onClick(clipboard)
                return 
            
    def _bp_increment(self) -> int:
        curr = self.buttonpos

        self.buttonpos += self.buttonsize + self.buttonspacing

        return curr

    def construct_buttons(self) -> None:
        size = self.buttonsize, self.buttonsize

        movementButton = Button.MovementButton(Rect((self._bp_increment(), self.buttonspacing), size), (200, 200, 0, 255))
        self.buttons.append(movementButton)

        penButton = Button.PenButton(Rect((self._bp_increment(), self.buttonspacing), size), (0, 200, 200, 255))
        self.buttons.append(penButton)

        eraserButton = Button.EraserButton(Rect((self._bp_increment(), self.buttonspacing), size), (200, 0, 200, 255))
        self.buttons.append(eraserButton)

        clearButton = Button.ClearButton(Rect((self._bp_increment(), self.buttonspacing), size), (200, 0, 0, 255))
        self.buttons.append(clearButton)

    


