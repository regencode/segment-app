import pygame
from Font import Font
from Display import Display

class Button(Display):
    def __init__(self, app, position, size, callback=None, callback_input=None, text="", font_size=20):
        super().__init__(app=app, position=position, size=size, text=text, font_size=font_size)
        self.callback = callback
        self.callback_input = callback_input

    def collidepoint(self, mouse_pos):
        return 

    def onclick(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.callback is not None:
            if self.callback_input is not None:
                self.callback(self.callback_input)
            else:
                self.callback()