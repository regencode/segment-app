import pygame
from Font import Font

class Display:
    def __init__(self, app, position, size, text="", top_text=False):
        self.app = app
        self.screen = app.screen
        self.positionX = position[0]
        self.positionY = position[1]
        self.width = size[0]
        self.height = size[1]
        self.color = "White"
        self.font = Font(size=20).font
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.text = text

        self.rect.center = (self.positionX, self.positionY)
        self.text_surface = self.font.render(self.text, True, "Black")
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        if top_text:
            self.text_rect = self.text_surface.get_rect(midbottom=self.rect.midtop)


    def blit_display(self):
        pygame.draw.rect(self.screen, self.color, self.rect) 
        self.screen.blit(self.text_surface, self.text_rect)
    
