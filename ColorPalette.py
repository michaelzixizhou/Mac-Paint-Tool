import pygame


class ColorPalette:
    x: int
    y: int
    w: int
    h: int
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.Surface((w, h))
        self.image.fill((128, 128, 128, 255))
        self.rad = h//2
        self.pwidth = w-self.rad*2
        for i in range(self.pwidth):
            color = pygame.Color(0)
            color.hsla = (int(360*i/self.pwidth), 100, 50, 100)
            pygame.draw.rect(self.image, color, (i+self.rad, h//3, 1, h-2*h//3))
        self.p = 0

    def get_color(self) -> pygame.Color:
        color = pygame.Color(0)
        color.hsla = (int(self.p * self.pwidth), 100, 50, 100)
        return color
    
    def resize(self, new_x: int) -> None:
        self.rect.x = new_x

    def update(self) -> None:
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_buttons[0] and self.rect.collidepoint(mouse_pos):
            self.p = (mouse_pos[0] - self.rect.left - self.rad) / self.pwidth
            self.p = (max(0, min(self.p, 1)))

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
        pygame.draw.circle(surface, self.get_color(), center, self.rect.height // 4)
        pygame.draw.circle(surface, (255, 255, 255), center, self.rect.height // 4, 2)


