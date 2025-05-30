import pygame
from os.path import join
from random import randint
import asyncio
import sys, platform

WINDOW_WIDTH, WINDOW_HEIGHT = 400, 600
FRAME_SIZE = 16

class SpriteHelper:
    def __init__(self, image_path: str):
        self.sprite = pygame.image.load(image_path).convert_alpha()
        self.sprite.set_colorkey((0, 0, 0))
    
    def get_frame(self, x: float, y: float, width: float, height: float):
        frame = pygame.Surface((width, height), pygame.SRCALPHA)
        frame.blit(self.sprite, (0,0), (x, y, width, height))
        return frame
    
class TextHelper:
    def __init__(self, text, color, size):
        self.text_value = text
        self.color = color
        pygame.font.init()
        self.text = pygame.font.Font(join('assets', 'text', 'Jersey15-Regular.ttf'), size=size)
        
    def render(self, screen, pos):
        self.text_surf = self.text.render(str(round(self.text_value, 0)), True, self.color)
        self.rect = self.text_surf.get_frect(center=pos)
        screen.blit(self.text_surf, self.rect)
        
    def set_score(self, num):
        self.text_value = num
        
class Music:
    def __init__(self, music_path):
        pygame.mixer.init()
        self.music = pygame.mixer.Sound(music_path)

    def play(self):
        self.music.play()