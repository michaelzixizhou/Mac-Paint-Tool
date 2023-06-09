from PIL import ImageGrab, Image
import pygame
import GUI
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
        self.scroll = 0

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
                image.display(self.screen)

        if self.selected_box:
            pygame.draw.rect(self.screen, (255, 0, 0), self.selected_box.get_rect(), 2)  
        
        for drawing in self.drawBoard.objs:
            if isinstance(drawing, DrawingLine):
                pygame.draw.line(self.screen, drawing.color, drawing.start, drawing.end, drawing.thickness)
      
        self.gui.display(self.screen, self.scroll)

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
        elif event.type ==  pygame.MOUSEBUTTONUP:
            self.moving = False
        elif event.type == pygame.MOUSEMOTION and self.moving:
            if self.selected_box:
                self.selected_box.move(event.rel)
    

    def drawingMode(self, event: pygame.event.Event, color: Union[tuple[int, int, int, int], pygame.Color], \
                     width: int = 3) -> None:
        """
        Draws and registers DrawingObjects to the clipboard with <color> and <width>.
        """
        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0]: # left mouse button
                last = (event.pos[0]-event.rel[0], event.pos[1]-event.rel[1])
                self.drawBoard.addLines(DrawingLine(color, last, event.pos, width))
        
    
    def eraserMode(self, event: pygame.event.Event, width: int = 30) -> None:
        """
        Erases DrawingObjects with a <width>-sized rectangle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.moving = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.moving = False
        elif event.type == pygame.MOUSEMOTION and self.moving:
            eraserRect = pygame.Rect(0, 0, width, width)
            eraserRect.center = event.pos
            
    
    def textMode(self, event: pygame.event.Event, color: pygame.Color = pygame.Color(255, 255, 255), 
                 font: str = "arialunicode", font_size: int = 30) -> None:
        """
        Creates TextBox objects to display text
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            temp = self.findImage(event.pos)
            if isinstance(temp, TextBox):
                self.selected_box = temp
                self.text = self.selected_box.text
            else:
                self.selected_box = TextBox(pygame.Rect(event.pos, (font_size, font_size)), color, font, font_size)
                self.addBox(self.selected_box)
                self.text = ''
        
        if event.type == pygame.KEYDOWN and isinstance(self.selected_box, TextBox):
            print("entered")
            if event.key == pygame.K_RETURN:
                self.selected_box = None
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            
            if self.selected_box:
                self.selected_box.change_text(self.text)

            print(self.text)

    def gui_control(self, event: pygame.event.Event) -> bool:
        clickedGUI = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickedGUI = self.gui.rect.collidepoint(event.pos)
            self.gui.button_press(event, self)
            selected_option = self.gui.dropdown.update(event, self.scroll)
            if selected_option >= 0:
                self.gui.dropdown.main = self.gui.dropdown.options[selected_option]
                self.font = self.gui.dropdown.get_option()
        elif event.type == pygame.MOUSEMOTION:
            self.gui.dropdown.menu_active = self.gui.dropdown.rect.collidepoint(event.pos)
        
            
        if self.gui.dropdown.draw_menu:
            if event.type == pygame.MOUSEWHEEL: 
                self.scroll = min(self.scroll + event.y * 15, 0)
            if event.type == pygame.MOUSEMOTION:
                self.gui.dropdown.update(event, self.scroll)

        return clickedGUI


    def event_loop(self) -> None:
        """
        Event loop keeps running until application is closed.

        Limited to 60 FPS
        """
        self.drawBoard = DrawingClipboard()
        self.gui = GUI.Interface(self.screen)
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
                        except AttributeError:
                            print("Not an image")
        

                if not self.gui_control(event):
                    match self.mode:
                        case "movement": 
                            self.movingMode(event)
                        case "drawing":
                            self.drawingMode(event, self.gui.palette.get_color())
                        case "eraser":
                            self.eraserMode(event)
                        case "text":
                            self.textMode(event, self.gui.palette.get_color(), self.font)
                        case _: # no matches
                            print("mode name does not exist")
                            self.mode = "movement"


            self.gui.palette.update()
            
            clock.tick(60)    
            self.render_screen()


if __name__ == "__main__":
    clipboard = Clipboard((1000, 800))

