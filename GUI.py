from pygame import Surface, Rect
import pygame
import Button
from ColorPalette import ColorPalette
from Dropdown import Dropdown
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS  # type: ignore
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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
    font_dropdown: Dropdown
    size_dropdown: Dropdown
    

    def __init__(self, screen: Surface, color: tuple[int, int, int, int] = (220, 220, 220, 255), \
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

        self.menuIsOpen = False
        
    def update_size(self) -> None:
        """
        Updates size of GUI in the case that the screen is resized.
        """
        self.rect = Rect((0, 0), (self.screen.get_width(), self.width))
        self.palette.resize(self.screen.get_width() - 300)

    def display(self, surface: Surface, scroll: int, mode: str) -> None:
        """
        Display the GUI on the pygame application.
        """
        pygame.draw.rect(surface, self.color, self.rect)

        for button in self.buttons:
            button.display(self.screen)
        
        self._show_mode(surface, mode)

        self.palette.display(surface)
        self.font_dropdown.display(surface, scroll)
        self.size_dropdown.display(surface, 0)


    def _find_button(self, name: type) -> Button.Button: # type: ignore
        for b in self.buttons:
            if isinstance(b, name):
                return b
        
    def _show_mode(self, surface: Surface, mode: str) -> None:
        match mode:
            case "movement": 
                pygame.draw.rect(surface, (242, 66, 54), self._find_button(Button.MovementButton).get_rect(), 3)
            case "drawing":
                pygame.draw.rect(surface, (242, 66, 54), self._find_button(Button.PenButton).get_rect(), 3)
            case "eraser":
                pygame.draw.rect(surface, (242, 66, 54), self._find_button(Button.EraserButton).get_rect(), 3)
            case "text":
                pygame.draw.rect(surface, (242, 66, 54), self._find_button(Button.TextButton).get_rect(), 3)
            case _: # no matches
                print("mode name does not exist")

    def button_press(self, event: pygame.event.Event, clipboard) -> int:
        """
        Check if a button is being pressed.
        """
        if self.font_dropdown.draw_menu or self.size_dropdown.draw_menu:
            self.menuIsOpen = True
        else:
            self.menuIsOpen = False

        for button in self.buttons:
            if button.get_rect().collidepoint(event.pos):
                return button.onClick()
        return 0
    
    def button_hover(self, event: pygame.event.Event, surface: Surface):
        for b in self.buttons:
            if b.rect.collidepoint(event.pos):
                pygame.draw.rect(surface, (100, 100, 100, 100), b.rect)
            
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
        # try:
        pygame.font.init()
        size = self.buttonsize, self.buttonsize

        movementButton = Button.MovementButton(Rect((self._bp_increment(), self.buttonspacing), size), (72, 99, 156, 255), pygame.image.load(resource_path("Sprites/CursorSprite.png")))
        self.buttons.append(movementButton)

        penButton = Button.PenButton(Rect((self._bp_increment(), self.buttonspacing), size), (76, 76, 157, 255), pygame.image.load(resource_path("Sprites/PenSprite.png")))
        self.buttons.append(penButton)

        eraserButton = Button.EraserButton(Rect((self._bp_increment(), self.buttonspacing), size), (113, 47, 121, 255), pygame.image.load(resource_path("Sprites/EraserSprite.png")))
        self.buttons.append(eraserButton)

        clearButton = Button.ClearButton(Rect((self._bp_increment(), self.buttonspacing), size), (151, 99, 145, 255), pygame.image.load(resource_path("Sprites/CrossSprite.png")))
        self.buttons.append(clearButton)

        textButton = Button.TextButton(Rect((self._bp_increment(), self.buttonspacing), size), (247, 153, 110, 255), pygame.image.load(resource_path("Sprites/TextSprite.png")))
        self.buttons.append(textButton)

        self.construct_font_dropdown()
        
        # smaller buttons
        textColorButton = Button.TextColorButton(Rect((self.buttonpos, 2 * self.buttonspacing + self.buttonsize // 3), 
                                                        (size[0] // 3 * 2 - self.buttonspacing, size[1] // 3 * 2 - self.buttonspacing)), 
                                                    (100, 100, 0, 255))
        self.buttonpos += size[0] // 3 * 2 
        self.buttons.append(textColorButton)
        self.text_color_button = textColorButton

        self.construct_font_size_dropdown()
        self.buttonpos += 70 + self.buttonspacing

        textApplyButton = Button.TextApplyButton(Rect((self.buttonpos, 2 * self.buttonspacing + self.buttonsize // 3), 
                                                        (size[0] // 3 * 2 - self.buttonspacing, size[1] // 3 * 2 - self.buttonspacing)), 
                                                    (248, 162, 123, 255), pygame.image.load(resource_path("Sprites/CheckSprite.png")))
        self.buttonpos += size[0] // 3 * 2 
        self.buttons.append(textApplyButton)

        # except Exception as e:
        #     print(e)

    def construct_palette(self) -> None:
        cp = ColorPalette(self.rect.width - 300, 0, 300, self.width)
        self.palette = cp

    def construct_font_dropdown(self) -> None:
        fonts = []
        for font in sorted(pygame.font.get_fonts()):
            if font[:4] == "noto":
                continue
            else:
                fonts.append(font)

        dd = Dropdown([(255, 255, 255, 255), (130, 130, 130, 255)], [(255, 255, 255, 255), (130, 130, 130, 255)], 
                      self.buttonpos, self.buttonspacing, 200, 
                      self.buttonsize // 3, pygame.font.Font(pygame.font.match_font("arialunicode"), 15), 
                      "arialunicode", fonts)
        self.font_dropdown = dd

        dd.active_option = dd.find_option_index("arialunicode")
        
    def construct_font_size_dropdown(self) -> None:
        size_list = []
        for i in range(0, 16):
            size_list.append(str(i + 1))
        for i in range(10):
            size_list.append(str((i+1) * 4 + 16))
        for i in range(5):
            size_list.append(str((i + 1) * 8 + 56))
        for i in range(5):
            size_list.append(str((i + 1) * 48 + 104))
        

        dd  = Dropdown([(255, 255, 255, 255), (130, 130, 130, 255)], [(255, 255, 255, 255), (130, 130, 130, 255)], 
                      self.buttonpos, 2 * self.buttonspacing + self.buttonsize // 3, 70, 
                      self.buttonsize // 3, pygame.font.Font(pygame.font.match_font("arialunicode"), 15), 
                      "32", size_list)
        dd.active_option = dd.find_option_index("32")

        self.size_dropdown = dd


