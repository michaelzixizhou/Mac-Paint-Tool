from pygame import Surface, Rect
import pygame
import Button
from ColorPalette import ColorPalette


class Interface():
    """
    GUI that stores all the buttons in the form of clickable rects

    Singleton that holds all Buttons.
    """
    color: tuple[int, int, int, int]
    rect: Rect
    buttons: list[Button.Button]
    screen: Surface
    width: int
    buttonsize: int
    buttonspacing: int
    buttonpos: int
    palette: ColorPalette
    

    def __init__(self, screen: Surface, color: tuple[int, int, int, int] = (128, 128, 128, 255), \
                 width: int = 70, buttonspacing: int = 5) -> None:
        self.color = color
        self.width = width
        self.rect = Rect((0, 0), (screen.get_width(), width))
        self.buttons = []
        self.screen = screen

        self.buttonspacing = buttonspacing
        self.buttonpos = buttonspacing
        self.buttonsize = width - 2 * buttonspacing

        self.construct_buttons()
        self.construct_palette()

    def update_size(self) -> None:
        """
        Updates size of GUI in the case that the screen is resized.
        """
        self.rect = Rect((0, 0), (self.screen.get_width(), self.width))
        self.palette.resize(self.screen.get_width() - 300)

    def display(self, surface: Surface) -> None:
        """
        Display the GUI on the pygame application.
        """
        pygame.draw.rect(surface, self.color, self.rect)

        for button in self.buttons:
            pygame.draw.rect(surface, button.color, button.rect)
        
        self.palette.draw(surface)

    def check_collision(self, event: pygame.event.Event, clipboard) -> None:
        """
        Check if a button is being pressed.
        """
        for button in self.buttons:
            if button.get_rect().collidepoint(event.pos):
                button.onClick(clipboard)
                return 
            
    def _bp_increment(self) -> int:
        """
        Helper function for construct_buttons for button placement.
        """
        curr = self.buttonpos

        self.buttonpos += self.buttonsize + self.buttonspacing

        return curr

    def construct_buttons(self) -> None:
        """
        Add the buttons in order from left to right on the GUI.
        """
        try:
            size = self.buttonsize, self.buttonsize

            movementButton = Button.MovementButton(Rect((self._bp_increment(), self.buttonspacing), size), (200, 200, 0, 255))
            self.buttons.append(movementButton)

            penButton = Button.PenButton(Rect((self._bp_increment(), self.buttonspacing), size), (0, 200, 200, 255))
            self.buttons.append(penButton)

            eraserButton = Button.EraserButton(Rect((self._bp_increment(), self.buttonspacing), size), (200, 0, 200, 255))
            self.buttons.append(eraserButton)

            clearButton = Button.ClearButton(Rect((self._bp_increment(), self.buttonspacing), size), (200, 0, 0, 255))
            self.buttons.append(clearButton)

        except Exception as e:
            print(e)
            print("buttons probably out of bounds")

    def construct_palette(self) -> None:
        cp = ColorPalette(self.rect.width - 300, 0, 300, self.width)
        self.palette = cp

