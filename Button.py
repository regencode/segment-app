import pygame
from Font import Font
from Display import Display
from Notification import Notification

class Button(Display):
    def __init__(self, app, position, size, callback=None, callback_input=None, text="", use_notif=False, notif_text="", font_size=20):
        super().__init__(app=app, position=position, size=size, text=text, font_size=font_size)
        self.callback = callback
        self.callback_input = callback_input
        self.use_notif = use_notif
        self.notification = None
        if self.use_notif:
            self.notification = Notification(self.app, (200, 650), size=(350, 50), text=notif_text, time_onscreen=3000)

    def onclick(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.callback is not None:
            if self.callback_input is not None:
                self.callback(self.callback_input)
            else:
                self.callback()
            if self.use_notif: 
                self.notification.show()