from PIL import ImageGrab, Image
import pyperclip
import pygame
from GUI import Interface
from typing import Optional, Union
from ImageObject import ImageObject
from Drawing import DrawingLine, DrawingClipboard
from TextBox import TextBox 


def getClipboardIMG(resize: float = 0, mousepos: tuple[int, int] = (0, 0)) -> Optional[ImageObject]:
    """
    Gets an image form clipboard and converts it to a pygame.Surface.
    Parameter <resize> controls the size of the Surface.
    """
    img = ImageGrab.grabclipboard()
    if not img:
        return None
    
    if resize:
        ratio = img.height / img.width
        new_w = img.width * resize
        new_h = new_w * ratio

        img = img.resize((int(new_w), int(new_h)), Image.LANCZOS)

    img = pygame.image.fromstring(img.tobytes(), img.size, img.mode) # type: ignore

    return ImageObject(img, mousepos)

def collideEdge(event: pygame.event.Event, rect: pygame.Rect) -> int:
    """
    Check if the mouse is hovering over the edge of a rect, for scaling purposes
    """
    w, h, x, y = rect.w, rect.h, rect.x, rect.y
    offset = 20
    edgerect = pygame.Rect(x - offset, y - offset, w + 2*offset, 2*offset)
    if edgerect.collidepoint(event.pos):
        return 1
    edgerect.y += h
    if edgerect.collidepoint(event.pos):
        return 2

    edgerect = pygame.Rect(x - offset, y - offset, 2*offset, h + 2* offset)
    if edgerect.collidepoint(event.pos):
        return 1
    edgerect.x += w 
    if edgerect.collidepoint(event.pos):
        return 2
    
    return 0

class Clipboard():
    """
    Clipboard application.

    Sets up and runs pygame.
    """
    
    res: tuple[int, int]
    boxes: list[Union[ImageObject, TextBox]]
    screen: pygame.Surface
    selected_box: Optional[Union[ImageObject, TextBox]]
    moving: bool
    drawBoard: DrawingClipboard
    mode: str


    def __init__(self, res: tuple[int, int]) -> None:
        """
        Runs the application at <res> resolution.

        Stores singletons of DrawingBoard and GUI.

        ===========================================
        Current modes:
        movement - interacting with image objects
        drawing - draws lines
        eraser - erases lines
        """
        self.res = res
        self.boxes = []
        self.selected_box = None
        self.moving = False
        self.mode = "movement"
        self.text = ''
        self.font = "arialunicode"
        self.font_size = 32
        self.scroll = 0
        self.pen_size = 3
        self.eraser_size = 32
        self.eraser_check = False
        self.resize = 0

        self.run_visualizer()
    
    def addBox(self, box: Union[ImageObject, TextBox]) -> None:
        """
        Adds <img> to the current canvas to be loaded and displayed
        """
        self.boxes.append(box)
    
    def findImage(self, point: tuple[int, int]) -> Optional[Union[ImageObject, TextBox]]:
        """
        Finds the image at <point> on the canvas and returns it, if there doesn't exist one, return None.
        """
        x, y = point
        for i in range(len(self.boxes) - 1, -1, -1):
            rect = self.boxes[i].get_rect()
            if rect.collidepoint(x, y):
                return self.boxes[i]
        return None
    
    def run_visualizer(self) -> None:
        """
        Runs the pygame visualizer with <res> as the resolution.
        """
        pygame.init()

        self.screen = pygame.display.set_mode(self.res, pygame.RESIZABLE)

        pygame.display.set_caption("Mac Paint")

        pygame.font.init()

        self.event_loop()

    def render_screen(self) -> None:
        """
        Renders images first, then drawings on top. Also highlights the selected image.
        """
        self.screen.fill((0, 0, 0))

        for image in self.boxes:
            if isinstance(image, ImageObject):
                self.screen.blit(image.image, image.get_rect())
            elif isinstance(image, TextBox):
                if image.text == '' and image != self.selected_box:
                    self.boxes.remove(image)
                image.display(self.screen)

        if self.selected_box:
            pygame.draw.rect(self.screen, (255, 255, 255), self.selected_box.get_rect(), 1)  
        
        for drawing in self.drawBoard.objs:
            if isinstance(drawing, DrawingLine):
                pygame.draw.line(self.screen, drawing.color, drawing.start, drawing.end, drawing.thickness)
      
        self.gui.display(self.screen, self.scroll, self.mode)

        ### Eraser cursor
        # if self.mode == "eraser":
        #     pygame.draw.circle(self.screen, (255, 255, 255), pygame.mouse.get_pos(), radius=5, width=2)

        pygame.display.flip()


    def movingMode(self, event: pygame.event.Event) -> None:
        """
        Mode to select and move images.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.selected_box = self.findImage(event.pos)
            # print(self.selected_img)
            if self.selected_box:
                self.moving = True
                if isinstance(self.selected_box, ImageObject):
                    self.resize = collideEdge(event, self.selected_box.rect)
                        
        elif event.type ==  pygame.MOUSEBUTTONUP:
            self.moving = False
            if self.resize:
                assert isinstance(self.selected_box, ImageObject)

                self.resize = 0
                self.selected_box.image = pygame.transform.scale(self.selected_box.image, (self.selected_box.rect.w, self.selected_box.rect.h))

        elif event.type == pygame.MOUSEMOTION and self.moving:
            if self.selected_box:
                match self.resize:
                    case 0:
                        self.selected_box.move(event.rel)
                    case 1:
                        assert isinstance(self.selected_box, ImageObject)

                        self.selected_box.rect.w -= event.rel[0]
                        self.selected_box.rect.h -= event.rel[1]
                        self.selected_box.rect.w = max(self.selected_box.rect.w, 10)
                        self.selected_box.rect.h = max(self.selected_box.rect.h, 10)    
                        self.selected_box.rect.x += event.rel[0]
                        self.selected_box.rect.y += event.rel[1]
                    case 2:
                        assert isinstance(self.selected_box, ImageObject)

                        self.selected_box.rect.w += event.rel[0]
                        self.selected_box.rect.h += event.rel[1]
                        self.selected_box.rect.w = max(self.selected_box.rect.w, 10)
                        self.selected_box.rect.h = max(self.selected_box.rect.h, 10)
                    

        if event.type == pygame.KEYDOWN and self.selected_box:
            if event.key == pygame.K_BACKSPACE:
                self.boxes.remove(self.selected_box)
                self.selected_box = None
            
    

    def drawingMode(self, event: pygame.event.Event, color: Union[tuple[int, int, int, int], pygame.Color], \
                     width: int = 3) -> None:
        """
        Draws and registers DrawingObjects to the clipboard with <color> and <width>.
        """
        if self.moving:
            self.pen_size = int(self.gui.size_dropdown.get_option())
            self.moving = False
        self.gui.size_dropdown.set_option(self.gui.size_dropdown.find_option_index(str(self.pen_size)))
        self.gui.size_dropdown.update(event, 0)

        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0]: # left mouse button
                last = (event.pos[0]-event.rel[0], event.pos[1]-event.rel[1])
                self.drawBoard.addLines(DrawingLine(color, last, event.pos, self.pen_size))
        
    
    def eraserMode(self, event: pygame.event.Event, width: int = 32) -> None:
        """
        Erases DrawingObjects with a <width>-sized rectangle.
        """
        if self.eraser_check:
            self.eraser_size = int(self.gui.size_dropdown.get_option())
            self.eraser_check= False
        self.gui.size_dropdown.set_option(self.gui.size_dropdown.find_option_index(str(self.eraser_size)))
        self.gui.size_dropdown.update(event, 0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.moving = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.moving = False
        elif event.type == pygame.MOUSEMOTION and self.moving:
            eraserRect = pygame.Rect(0, 0, self.eraser_size, self.eraser_size)
            eraserRect.center = event.pos
            self.drawBoard.eraseAt(eraserRect)
            
    
    def textMode(self, event: pygame.event.Event, color: pygame.Color = pygame.Color(255, 255, 255), 
                 font: str = "arialunicode", font_size: int = 32) -> None:
        """
        Creates TextBox objects to display text
        """
        if event.type == pygame.MOUSEBUTTONDOWN and not self.moving:
            temp = self.findImage(event.pos)
            if isinstance(temp, TextBox):
                self.selected_box = temp
                self.text = self.selected_box.text
            else:
                self.selected_box = TextBox(pygame.Rect(event.pos, (self.font_size, self.font_size)), color, self.font, self.font_size)
                self.addBox(self.selected_box)
                self.text = ''

            self._update_text_dropdowns()
            
        
        if event.type == pygame.KEYDOWN and isinstance(self.selected_box, TextBox):  
            if event.key == pygame.K_RETURN:
                self.selected_box = None
            elif (event.key == pygame.K_BACKSPACE) and (event.mod & pygame.KMOD_META):
                self.text = ''
            elif (event.key == pygame.K_c) and (event.mod & pygame.KMOD_META):
                pyperclip.copy(self.text)
            elif (event.key == pygame.K_v) and (event.mod & pygame.KMOD_META):
                self.text += pyperclip.paste()
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            
            if self.selected_box:
                self.selected_box.change_text(self.text)

        if isinstance(self.selected_box, TextBox) and self.moving:
            print("entered")
            self.selected_box.color = self.gui.text_color_button.color
            self.selected_box.font = self.font
            
            self.selected_box.font_size = int(self.gui.size_dropdown.get_option())
            print(self.selected_box.font_size)
            
            self._update_text_dropdowns()

            self.moving = False

    def _update_text_dropdowns(self) -> None:
        assert isinstance(self.selected_box, TextBox)
        self.font = self.selected_box.font
        self.font_size = self.selected_box.font_size
        self.color = self.selected_box.color

        self.gui.font_dropdown.set_option(self.gui.font_dropdown.find_option_index(self.font))
        self.gui.size_dropdown.set_option(self.gui.size_dropdown.find_option_index(str(self.font_size)))

        self.gui.text_color_button.color = self.color


    def gui_control(self, event: pygame.event.Event) -> bool:
        """
        Handles all GUI work
        """

        clickedGUI = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickedGUI = self.gui.rect.collidepoint(event.pos)
            b = self.gui.button_press(event, self)
            if b:
                print(self.mode)
                match b:
                    case 1:
                        self.mode = "drawing"
                    case 2:
                        self.mode = "eraser"
                        print("in")

                    case 3:
                        self.mode = "movement"
                    case 4:
                        self.drawBoard.clearBoard()
                        self.boxes = []
                    case 5:
                        self.mode = "text"
                    case 6:
                        self.color = self.gui.palette.get_color()
                        self.gui.text_color_button.color = self.color
                    case 7:
                        self.moving = True
                        self.eraser_check = True
                    

            font_option = self.gui.font_dropdown.update(event, self.scroll)
            if font_option >= 0:
                self.gui.font_dropdown.main = self.gui.font_dropdown.options[font_option]
                self.font = self.gui.font_dropdown.get_option()

            fontsize_option = self.gui.size_dropdown.update(event, 0)
            if fontsize_option >= 0:
                self.gui.size_dropdown.main = self.gui.size_dropdown.options[fontsize_option]
                self.font_size = int(self.gui.size_dropdown.get_option())
        
        if event.type == pygame.MOUSEMOTION:
            self.gui.font_dropdown.menu_active = self.gui.font_dropdown.rect.collidepoint(event.pos)
            self.gui.size_dropdown.menu_active = self.gui.size_dropdown.rect.collidepoint(event.pos)
            
        if self.gui.font_dropdown:
            if self.gui.font_dropdown.draw_menu:
                if event.type == pygame.MOUSEWHEEL: 
                    self.scroll = min(self.scroll + event.y * 20, 0)
                if event.type == pygame.MOUSEMOTION:
                    self.gui.font_dropdown.update(event, self.scroll)
            elif self.gui.size_dropdown.draw_menu:
                if event.type == pygame.MOUSEMOTION:
                    self.gui.size_dropdown.update(event, 0)

        return clickedGUI


    def event_loop(self) -> None:
        """
        Event loop keeps running until application is closed.

        Limited to 60 FPS
        """
        self.drawBoard = DrawingClipboard()
        self.gui = Interface(self.screen)
        clock = pygame.time.Clock()
        pygame.mouse.set_cursor(pygame.cursors.diamond)

        while (True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.gui.update_size()

                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_v) and (event.mod & pygame.KMOD_META):
                        try:
                            img = getClipboardIMG(0.5, pygame.mouse.get_pos())
                            if img:
                                self.addBox(img)
                                self.selected_box = img
                            else:
                                self.selected_box = TextBox(pygame.Rect(event.pos, (self.font_size, self.font_size)), 
                                                            self.gui.palette.get_color(), self.font)
                                self.addBox(self.selected_box)
                                self.mode = "text"
                                
                        except AttributeError:
                            print("Not an image")
                        

                if not self.gui_control(event) and not self.gui.menuIsOpen:
                    match self.mode:
                        case "movement": 
                            self.movingMode(event)
                        case "drawing":                            
                            self.drawingMode(event, self.gui.palette.get_color())
                        case "eraser":
                            self.eraserMode(event)
                        case "text":
                            if not self.gui.font_dropdown.draw_menu and not self.gui.size_dropdown.draw_menu:
                                self.textMode(event, self.gui.palette.get_color(), self.font)
                        case _: # no matches
                            print("mode name does not exist")
                            self.mode = "movement"


            self.gui.palette.update()
            
            clock.tick(60)    
            self.render_screen()
            


if __name__ == "__main__":
    s = pygame.Surface((10, 10))
    i = Interface(s)
    clipboard = Clipboard((1000, 800))

