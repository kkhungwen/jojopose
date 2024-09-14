import pygame
import time

class FlashingText:
    def __init__(self, font, flash_interval=0.5):
        self.font = font
        self.flash_interval = flash_interval
        self.last_flash_time = time.time()
        self.flash_state = True

    def update(self, screen, text, position, color1, color2):
        current_time = time.time()
        if current_time - self.last_flash_time > self.flash_interval:
            self.flash_state = not self.flash_state
            self.last_flash_time = current_time
        
        color = color1 if self.flash_state else color2
        flashed_text = self.font.render(text, True, color)
        text_rect = flashed_text.get_rect(center=position)
        screen.blit(flashed_text, text_rect)
