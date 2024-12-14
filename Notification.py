import pygame
from Display import Display
import time

class Notification(Display): # blit only when needed
    def __init__(self, app, position, size, time_onscreen=1500, text="hello", font_size=20):
        super().__init__(app=app, position=position, size=size, text=text, font_size=font_size)
        self.time_onscreen = time_onscreen 
        self.time_ctr = 0

    def blit(self):
        if self.time_ctr > 0:
            pygame.draw.rect(self.screen, self.color, self.rect) 
            if self.display_content is not None:
                self.screen.blit(self.display_content, self.display_content_rect)
            self.screen.blit(self.text_surface, self.text_rect)
            self.time_ctr -= 2
        else:
            return

    def show(self):
        self.time_ctr = self.time_onscreen
    