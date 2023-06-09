import pygame


class ColorPalette:
    """
    Color palette with a hue and lightness (greyscale) slider.
    """
    x: int
    y: int
    w: int
    h: int
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        self.rect1 = pygame.Rect(x, y, w, h//2)
        self.rect2 = pygame.Rect(x, h//2, w, h//2)
        self.image1 = pygame.Surface((w, h//2))
        self.image1.fill((220, 220, 220, 255))
        self.image2 = pygame.Surface((w, h//2))
        self.image2.fill((220, 220, 220, 255))

        self.rad = 10
        self.pwidth = w-self.rad*2
        
        for i in range(self.pwidth):
            color = pygame.Color(0)
            color.hsla = (int(360*i/self.pwidth), 100, 50, 100)
            pygame.draw.rect(self.image1, color, (i+self.rad, 10, 1, 10))

        for j in range(self.pwidth):
            grey = pygame.Color(0)
            grey.hsla = (0, 0, int((100 * j / self.pwidth)), 100)
            pygame.draw.rect(self.image2, grey, (j+self.rad, 16, 1, 10))

        self.p1 = 0
        self.p2 = 0.5

    def get_saturation(self) -> pygame.Color:
        color = pygame.Color(0)
        color.hsla = (int(self.p1 * 360), 100, 50, 100)
        return color
    
    def get_lightness(self) -> pygame.Color:
        color = pygame.Color(0)
        color.hsla = (0, 0, (int(self.p2 * 100)), 0)
        return color
    
    def get_color(self) -> pygame.Color:
        h = self.get_saturation().hsla[0]
        l = self.get_lightness().hsla[2]
        color = pygame.Color(0)
        color.hsla = (h, 100, l, 100)
        return color
    
    def resize(self, new_x: int) -> None:
        self.rect1.x = new_x
        self.rect2.x = new_x

    def update(self) -> None:
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_buttons[0] and self.rect1.collidepoint(mouse_pos):
            self.p1 = (mouse_pos[0] - self.rect1.left - self.rad) / self.pwidth
            self.p1 = (max(0, min(self.p1, 1)))

        elif mouse_buttons[0] and self.rect2.collidepoint(mouse_pos):
            self.p2 = (mouse_pos[0] - self.rect1.left - self.rad) / self.pwidth
            self.p2 = (max(0, min(self.p2, 1)))

    def display(self, surface: pygame.Surface) -> None:
        surface.blit(self.image1, self.rect1)
        center1 = self.rect1.left + self.rad + self.p1 * self.pwidth, self.rect1.top + 15
        pygame.draw.circle(surface, self.get_saturation(), center1, self.rect1.height // 4)
        pygame.draw.circle(surface, (255, 255, 255), center1, self.rect1.height // 4, 2)

        surface.blit(self.image2, self.rect2)
        center2 = self.rect2.left + self.rad + self.p2 * self.pwidth, self.rect2.top + 21
        pygame.draw.circle(surface, self.get_lightness(), center2, self.rect2.height // 4)
        pygame.draw.circle(surface, (255, 255, 255), center2, self.rect2.height // 4, 2)

        center3 = self.rect1.left + (self.rect1.right - self.rect1.left) // 2, self.rect2.centery - self.rect1.centery
        
        pygame.draw.circle(surface, self.get_color(), center3, 13)
        pygame.draw.circle(surface, (0, 0, 0, 0), center3, 13, 1)

        pygame.draw.rect(self.image1, (0, 0, 0), (self.rad, 10, self.pwidth, 10), 1)
        pygame.draw.rect(self.image2, (0, 0, 0), (self.rad, 16, self.pwidth, 10), 1)

        
        

