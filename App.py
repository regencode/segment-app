import pygame, sys, os
import cv2 as cv
from Settings import Settings
from GUI import GUI


class SegmentApp:

    def __init__(self):
        pygame.init()
        self.running = True
        self.global_tick = pygame.time.get_ticks()
        self.settings = Settings()
        self.width = self.settings.display_size[0]
        self.height = self.settings.display_size[1]
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.width, self.height), depth=16)
        self.screen_rect = self.screen.get_rect()

        self.gui = GUI(self, self.width, self.height)

        self.screen.fill("Gray")

        pygame.display.set_caption("Brain Tumor Segmentation")

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                self.gui.register_click(mouse_pos)

    
    def display_objects(self):
        self.gui.display_title()
        self.gui.display_button()

    def run(self):
        # infinite event loop
        while self.running:
            self.global_tick = pygame.time.get_ticks()
            self.screen.fill("Gray")

            self.check_events() # Check for events such as user inputs
            self.display_objects()

            pygame.display.flip()


if __name__ == "__main__":
    app = SegmentApp()
    app.run()
