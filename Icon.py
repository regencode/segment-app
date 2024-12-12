import pygame

class Icon:
    def __init__(self, app, icon_path, position):
        self.app = app
        self.screen = app.screen

        self.image = pygame.image.load(icon_path).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.3)
        self.rect = self.image.get_rect(center = position)

    def blit(self):
        self.screen.blit(self.image, self.rect)