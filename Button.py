import pygame
from Font import Font
from Display import Display

class Button(Display):
    def __init__(self, app, text, position, size, callback):
        super().__init__(app, text, position, size)
        self.callback = callback

    def collidepoint(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def onclick(self, mouse_pos):
        if self.collidepoint(mouse_pos) and self.callback is not None:
            self.callback()