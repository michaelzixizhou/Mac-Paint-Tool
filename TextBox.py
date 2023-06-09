import pygame
from typing import Union


class TextBox():
    text: str
    font: str
    rect: pygame.Rect
    color: Union[pygame.Color, tuple[int, int, int, int]]
    font_size: int

    def __init__(self, rect: pygame.Rect, color: pygame.Color = pygame.Color(255, 255, 255), 
                 font: str = "arialunicode", font_size: int = 30) -> None:
        self.text = ""
        self.rect = rect
        self.color = color
        self.font = font
        self.font_size = font_size
    
    def move(self, pos: tuple[int, int]):
        self.rect.move_ip(pos[0], pos[1])

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def change_text_size(self, new_size: int) -> None:
        self.font_size = new_size

    def change_font(self, new_font: str) -> None:
        self.font = new_font
    
    def change_text(self, new_text: str) -> None:
        self.text = new_text

    def change_color(self, new_color: Union[pygame.Color, tuple[int, int, int, int]]) -> None:
        self.color = new_color

    def display(self, screen: pygame.Surface) -> None:
        try:
            font = pygame.font.Font(pygame.font.match_font(self.font), self.font_size)
        except ValueError:
            print("font not found")
            font = pygame.font.Font(pygame.font.match_font("arialunicode"), self.font_size)

        text_surface = font.render(self.text, False, self.color)
        width = max(200, text_surface.get_width()+10)
        self.rect.w = width
        height = max(30, text_surface.get_height()+5)
        self.rect.h = height
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
