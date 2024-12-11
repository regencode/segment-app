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
        self.font = Font(size=40).font
        self.center_x = self.width//2
        self.center_y = self.height//2
        self.buttons = None
        self.displays = None

        self.init_objects()
    
    def add(self):
        self.ctr += 1
    
    def init_objects(self):
        self.buttons = [
            Button(self.app, position=(self.center_x, self.center_y+250), size=(180, 80), callback=self.add, text="Segment")
        ]
        self.displays = [
            Display(self.app, position=(self.center_x//2, self.center_y-50), size=(300, 300), text="Input", top_text=True),
            Display(self.app, position=(self.center_x//2+self.center_x, self.center_y-50), size=(300, 300), text="Output", top_text=True),
        ]
    
    def register_click(self, mouse_pos):
        for button in self.buttons:
            button.onclick(mouse_pos)
    
    def show_objects(self):
        self.show_title()
        self.show_objects()
        
    def show_title(self):
        self.title = self.font.render(f"Brain Tumor Segmentation", True, "Black")
        self.title_rect = self.title.get_rect(midtop = self.screen_rect.midtop)
        self.screen.blit(self.title, self.title_rect)
    
    def show_objects(self):
        for button in self.buttons:
            button.blit_display()
        for display in self.displays:
            display.blit_display()


