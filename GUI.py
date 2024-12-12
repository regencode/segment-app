import pygame
from Button import Button
from Display import Display
from Font import Font
from Icon import Icon
from Popup import Popup

import numpy as np



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
        self.font_smaller = Font(size=25).font
        self.center_x = self.width//2
        self.center_y = self.height//2
        self.buttons = None
        self.displays = None
        
        self.numpy_random = np.random.randint(0, 255, (255, 255, 3))

        self.mode_selection_popup = Popup(self.app, position=(self.center_x, self.center_y+20), size=(800, 600), title="Methods:")

        self.init_objects()
    
        self.segment_state = 0 
        # 0 -> Watershed
        # 1 -> K-means
        # 2 -> U-net
        # 3 -> DeepLabV3+
    
    def init_objects(self):
        self.buttons = [
            Button(self.app, position=(self.center_x, self.center_y+250), size=(180, 80), callback=None, text="Segment"),
            Button(self.app, position=(self.center_x, self.center_y+160), size=(180, 80), callback=self.mode_selection_popup.toggle_visible, text="Method selection")
        ]
        self.displays = [
            Display(self.app, position=(self.center_x//2, self.center_y-50), size=(300, 300), text="Input", top_text=True, display_array=self.numpy_random),
            Display(self.app, position=(self.center_x//2+self.center_x, self.center_y-50), size=(300, 300), text="Output", top_text=True),
        ]
        self.icons = [
            Icon(self.app, "resources/right-arrow.png", position=(self.center_x, self.center_y-50))
        ]

    def fetch_state(self):
        self.segment_state = self.mode_selection_popup.get_state()
    
    def register_click(self, mouse_pos):
        if self.mode_selection_popup.visible:
            self.mode_selection_popup.register_click(mouse_pos)
        else:
            for button in self.buttons:
                button.onclick(mouse_pos)

    def segment_state_text(self):
        if self.segment_state == 0:
            return "Watershed segmentation"
        elif self.segment_state == 1:
            return "K-Means segmentation"
        elif self.segment_state == 2:
            return "U-Net segmentation"
        elif self.segment_state == 3:
            return "DeepLabV3+ segmentation"
    
    def show(self): # order matters, as the latest shown object will be at the top
        self.show_title()
        self.show_objects()
        self.show_icons()
        self.show_popups()
        
    def show_title(self):
        self.title = self.font.render(f"Brain Tumor Segmentation", True, "Black")
        self.title_rect = self.title.get_rect(midtop = self.screen_rect.midtop)
        self.screen.blit(self.title, self.title_rect)

        self.state_title = self.font_smaller.render(f"Selected method: {self.segment_state_text()}", True, "Black")
        self.state_title_rect = self.state_title.get_rect(midtop = self.title_rect.midbottom)
        self.screen.blit(self.state_title, self.state_title_rect)
    
    def show_objects(self):
        for button in self.buttons:
            button.blit()
        for display in self.displays:
            display.blit()
    
    def show_icons(self):
        for icon in self.icons:
            icon.blit()
    
    def show_popups(self):
        self.mode_selection_popup.blit()

