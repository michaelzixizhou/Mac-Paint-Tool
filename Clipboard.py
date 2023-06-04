from PIL import ImageGrab, Image
import pygame
from typing import Optional
from ImageObject import ImageObject
from Drawing import DrawingObject, DrawingClipboard


def getClipboardIMG(resize: float = 0, mousepos: tuple[int, int] = (0, 0)) -> ImageObject:
    """
    Gets an image form clipboard and converts it to a pygame.Surface.
    Parameter <resize> controls the size of the Surface.
    """
    img = ImageGrab.grabclipboard()
    
    if resize:
        ratio = img.height / img.width
        new_w = img.width * resize
        new_h = new_w * ratio

        img = img.resize((int(new_w), int(new_h)), Image.LANCZOS)

    img = pygame.image.fromstring(img.tobytes(), img.size, img.mode)

    return ImageObject(img, mousepos)


class Clipboard():
    """
    Clipboard application
    """
    images: list[ImageObject]

    def __init__(self) -> None:
        self.images = []
        self.screen = None
        self.selected_img = None
        self.moving = False
        self.drawBoard = None
        self.mode = "eraser"
    
    def addImage(self, img: ImageObject) -> None:
        self.images.append(img)
    
    def findImage(self, point: tuple[int, int]) -> Optional[ImageObject]:
        x, y = point
        for i in range(len(self.images) - 1, -1, -1):
            rect = self.images[i].get_rect()
            if rect.collidepoint(x, y):
                return self.images[i]
        return None
    
    def run_visualizer(self, res: tuple[int, int]) -> None:
        """
        Runs the pygame visualizer with <res> as the resolution.
        """
        pygame.init()

        self.screen = pygame.display.set_mode(res, pygame.RESIZABLE)

        pygame.display.set_caption("Clipboard")

        self.event_loop()


    def render_screen(self) -> None:
        """
        Renders images first, then drawings on top. Also highlights the selected image.
        """
        self.screen.fill((0, 0, 0))

        for image in self.images:
            self.screen.blit(image.image, image.get_rect())

        if self.selected_img:
            pygame.draw.rect(self.screen, (255, 0, 0), self.selected_img.get_rect(), 2)  
        
        for drawing in self.drawBoard.lines:
            pygame.draw.line(self.screen, drawing.color, drawing.start, drawing.end, drawing.thickness)

        if self.mode == "eraser":
            pygame.draw.circle(self.screen, (255, 255, 255), pygame.mouse.get_pos(), radius=5, width=2)

        pygame.display.flip()


    def movingMode(self, event: pygame.event.Event) -> None:
        """
        Mode to select and move images.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.selected_img = self.findImage(event.pos)
            print(self.selected_img)
            if self.selected_img:
                self.moving = True
        elif event.type ==  pygame.MOUSEBUTTONUP:
            self.moving = False
        elif event.type == pygame.MOUSEMOTION and self.moving:
            try:
                self.selected_img.move(event.rel)
            except AttributeError:
                print("nothing selected")
    

    def drawingMode(self, event: pygame.event.Event, color: tuple[int, int, int, int] = (255, 255, 255, 255), width: int = 2) -> None:
        """
        Draws and registers DrawingObjects to the clipboard with <color> and <width>
        """
        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0]: # left mouse button
                last = (event.pos[0]-event.rel[0], event.pos[1]-event.rel[1])
                self.drawBoard.addLines(DrawingObject(color, last, event.pos, width))

    
    def eraserMode(self, event: pygame.event.Event, width: int = 30) -> None:
        """
        Erases DrawingObjects with a <width>-sized rectangle
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.moving = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.moving = False
        elif event.type == pygame.MOUSEMOTION and self.moving:
            eraserRect = pygame.Rect(0, 0, width, width)
            eraserRect.center = event.pos
            self.drawBoard.eraseAt(eraserRect)
        

    def event_loop(self) -> None:
        """
        Event loop keeps running until application is closed.

        Limited to 60 FPS
        """
        self.drawBoard = DrawingClipboard()
        clock = pygame.time.Clock()

        while (True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_v) and (event.mod & pygame.KMOD_META):
                        try:
                            img = getClipboardIMG(0.5, pygame.mouse.get_pos())
                            if img:
                                self.addImage(img)
                                self.selected_img = img
                        except AttributeError:
                            print("Not an image")
                    elif (event.key == pygame.K_c):
                        self.mode = "movement"
                    elif (event.key == pygame.K_d):
                        self.mode = "drawing"
                    elif (event.key == pygame.K_e):
                        self.mode = "eraser"

                match self.mode:
                    case "movement": 
                        self.movingMode(event)
                    case "drawing":
                        self.drawingMode(event)
                    case "eraser":
                        self.eraserMode(event)

            clock.tick(60)    
            self.render_screen()



if __name__ == "__main__":
    clipboard = Clipboard()
    clipboard.run_visualizer((1000, 800))

