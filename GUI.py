import pygame
import os
import re
import cv2 as cv
from Button import Button
from Display import Display
from Font import Font
from Icon import Icon
from Popup import Popup


from utils.Watershed import watershed
from utils.KMeans import kmeans
from utils.UNet import UNetRunner
from utils.DeepLab import DeepLabRunner

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

        self.unet = UNetRunner('cpu')
        self.deeplab = DeepLabRunner('cpu')
        
        self.numpy_random = np.random.randint(0, 255, (256, 256, 3))
        self.input_folder = "TCGA_CS_4941_19960909"
        self.input_paths = []
        self.input_list_index = 0

        self.load_inputs_from_folder()
        self.input = cv.imread(self.input_paths[self.input_list_index])
        self.output = None

        self.input_display = Display(self.app, position=(self.center_x//2, self.center_y-50), size=(300, 300), text="Input", top_text=True, display_array=self.input)

        self.output_display = Display(self.app, position=(self.center_x//2+self.center_x, self.center_y-50), size=(300, 300), text="Output", top_text=True)

        self.mode_selection_popup = Popup(self.app, position=(self.center_x, self.center_y+20), size=(800, 600), title="Methods:")

    
        self.segment_state = 0 
        # 0 -> Watershed
        # 1 -> K-means
        # 2 -> U-net
        # 3 -> DeepLabV3+

        self.init_objects()

    

    def next_image(self):
        if self.input_list_index < len(self.input_paths) - 1:
            self.input_list_index += 1

            self.input = cv.imread(self.input_paths[self.input_list_index])
            self.input_display.update_display(self.input)

    def last_image(self):
        if self.input_list_index > 0:
            self.input_list_index -= 1
            self.input = cv.imread(self.input_paths[self.input_list_index])
            self.input_display.update_display(self.input)

    def load_inputs_from_folder(self):
        for idx, file_path in enumerate(os.listdir(self.input_folder)):
            if not re.match(".*_mask\.tif$", file_path):
                full_path = self.input_folder + "/" + file_path
                self.input_paths.append(full_path)

    def segment_input(self):
        if self.segment_state == 0:
            self.output = watershed(self.input, )
        elif self.segment_state == 1:
            self.output = kmeans(self.input,)
        elif self.segment_state == 2:
            self.output = self.unet.forward(self.input)
        elif self.segment_state == 3:
            self.output = self.deeplab.forward(self.input)
        # self.output should be numpy array
        self.output_display.update_display(self.output)  # update output display to show segmented image
    
    def init_objects(self):
        self.buttons = [
            Button(self.app, position=(self.center_x//2+180, self.center_y-50), size=(50, 50), text=">", callback=self.next_image),
            Button(self.app, position=(self.center_x//2-180, self.center_y-50), size=(50, 50), text="<", callback=self.last_image),
            Button(self.app, position=(self.center_x, self.center_y+250), size=(180, 80), callback=self.segment_input, text="Segment"),
            Button(self.app, position=(self.center_x, self.center_y+160), size=(180, 80), callback=self.mode_selection_popup.toggle_visible, text="Method selection")
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
        self.input_display.blit()
        self.output_display.blit()

    def show_icons(self):
        for icon in self.icons:
            icon.blit()
    
    def show_popups(self):
        self.mode_selection_popup.blit()

