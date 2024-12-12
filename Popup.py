import pygame
from Font import Font
from Button import Button

class Popup:
    def __init__(self, app, position, size, title):
        self.app = app;
        self.screen = app.screen
        self.font = Font(size=30).font
        self.posX = position[0]
        self.posY = position[1]
        self.width = size[0]
        self.height = size[1]
        self.color = "Gray"
        self.border_color = "Black"

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.posX, self.posY)

        self.border_rect = pygame.Rect(0, 0, self.width, self.height)
        self.border_rect.center = (self.posX, self.posY)

        self.title = self.font.render(title, True, "Black")
        self.title_rect = self.title.get_rect(midtop = self.rect.midtop)
        self.state = 0

        self.buttons = []
        self.visible = False
        self.init_objects()


    def debug(self):
        print("clicked")

    
    def toggle_visible(self): # used for button callback
        self.visible = not self.visible
    
    def register_click(self, mouse_pos):
        for button in self.buttons:
            button.onclick(mouse_pos)
    
    def get_state(self):
        return self.state 
    
    def update_state(self, new):
        self.state = new
    
    def init_objects(self):
        self.buttons = [
            Button(self.app, (self.posX, self.posY-200), size=(300, 90), text="Watershed Segmentation", callback=self.update_state, callback_input=0), 
            Button(self.app, (self.posX, self.posY-100), size=(300, 90), text="K-Means Segmentation", callback=self.update_state, callback_input=1), 
            Button(self.app, (self.posX, self.posY), size=(300, 90), text="U-Net Segmentation", callback=self.update_state, callback_input=2), 
            Button(self.app, (self.posX, self.posY+100), size=(300, 90), text="DeepLabV3+ Segmentation", callback=self.update_state, callback_input=3), 

            Button(self.app, (self.posX, self.posY+260), size=(200, 40), text="Back", callback=self.toggle_visible, font_size=15), 
        ]
    
    def blit(self):
        if self.visible:
            pygame.draw.rect(self.screen, self.color, self.rect)
            pygame.draw.rect(self.screen, self.border_color, self.border_rect, width=3)
            self.screen.blit(self.title, self.title_rect)
            self.show_buttons()

    def show_buttons(self):
        for button in self.buttons:
            button.blit()
    