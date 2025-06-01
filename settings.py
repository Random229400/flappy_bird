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
    def __init__(self, text, color, size, pos):
        self.text_value = text
        self.color = color
        self.pos = pos
        pygame.font.init()
        self.text = pygame.font.Font(join('assets', 'text', 'Jersey15-Regular.ttf'), size=size)
        self.text_surf = self.text.render(str(self.text_value), True, self.color)
        self.rect = self.text_surf.get_frect(center=(pos))
        
    def render(self, screen):
        self.text_surf = self.text.render(str(self.text_value), True, self.color)
        self.rect = self.text_surf.get_frect(center=(self.pos))
        screen.blit(self.text_surf, self.rect)
        
    def set_score(self, num):
        self.text_value = num
        
class Music:
    def __init__(self, music_path):
        pygame.mixer.init()
        self.music = pygame.mixer.Sound(music_path)

    def play(self):
        self.music.play()