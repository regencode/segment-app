import pygame
from Button import Button
from Display import Display
from Font import Font



class GUI:
    def __init__(self, app, width, height):
        self.app = app
        self.width = width
        self.height = height
        self.screen = app.screen
        self.screen_rect = app.screen_rect
        self.clock = app.clock
        self.settings = app.settings
        self.buttons = None
        self.font = Font(size=40).font
        self.center_pos = (self.width//2, self.height//2)
        self.ctr = 0

        self.init_objects()
    
    def add(self):
        self.ctr += 1
    
    def init_objects(self):
        self.buttons = [
            Button(self.app, text="Button", position=self.center_pos, size=(200, 120), callback=self.add)
        ]
    
    def register_click(self, mouse_pos):
        for button in self.buttons:
            button.onclick(mouse_pos)
        
    def display_title(self):
        self.title = self.font.render(f"Brain Tumor Segmentation{self.ctr}", True, "Black")
        self.title_rect = self.title.get_rect(midtop = self.screen_rect.midtop)
        self.screen.blit(self.title, self.title_rect)
    
    def display_button(self):
        for button in self.buttons:
            button.blit_display()


