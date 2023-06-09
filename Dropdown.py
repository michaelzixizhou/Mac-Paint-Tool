import pygame
from typing import Union


class Dropdown():

    def __init__(self, color_menu: list[Union[tuple[int, int, int, int], pygame.Color]], 
                 color_option: list[Union[tuple[int, int, int, int], pygame.Color]], x: int, y: int, w: int, h: int, 
                 font: pygame.font.FontType, main: str, options: list[str]) -> None:
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def display(self, surface: pygame.Surface, scroll: int) -> None:
        pygame.draw.rect(surface, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, True, (0, 0, 0))
        surface.blit(msg, msg.get_rect(center = self.rect.center))
        
        pygame.draw.polygon(surface, (0, 0, 0), [(self.rect.right - 5, self.rect.top + 5), 
                                                       (self.rect.right - 21, self.rect.top + 5),
                                                       (self.rect.right - 13, self.rect.bottom - 5)])
        
        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += ((i+1) * self.rect.height) + scroll
                pygame.draw.rect(surface, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, True, (0, 0, 0))
                surface.blit(msg, msg.get_rect(center = rect.center))
        
        


    def update(self, event: pygame.event.Event, scroll: int) -> int:
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height + scroll
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            elif self.draw_menu and self.active_option >= 0:
                self.draw_menu = False
                return self.active_option
            
        return -1
    
    def get_option(self) -> str:
        return self.options[self.active_option]