import pygame
from Font import Font

class Display:
    def __init__(self, app, position, size, text="", top_text="", font_size=20, display_array=None):
        self.app = app
        self.screen = app.screen
        self.posX = position[0]
        self.posY = position[1]
        self.width = size[0]
        self.height = size[1]
        self.color = "White"
        self.font = Font(size=font_size).font
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.posX, self.posY)

        self.text_surface = self.font.render(text, True, "Black")
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        if top_text:
            self.text_rect = self.text_surface.get_rect(midbottom=self.rect.midtop)

        self.display_content = None
        self.display_content_rect = None
        if display_array is not None:
            self.display_content = pygame.surfarray.make_surface(display_array)
            self.display_content_rect = self.display_content.get_rect(center=self.rect.center)


    def blit(self):
        pygame.draw.rect(self.screen, self.color, self.rect) 
        if self.display_content is not None:
            self.screen.blit(self.display_content, self.display_content_rect)
        self.screen.blit(self.text_surface, self.text_rect)
    
