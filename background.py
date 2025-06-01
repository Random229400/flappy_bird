from typing import Any
from settings import *

class Background(pygame.sprite.Sprite):
    def __init__(self, groups, sprites, pos, layer):
        self._layer = layer
        super().__init__()
        self.add(groups)
        self.groups = groups
        self.sprites = sprites
        self.image = self.sprites[randint(0, len(sprites) - 1)]
        self.image = pygame.transform.scale(self.image, (400, 600))
        self.rect = self.image.get_frect(midleft=pos)
    
    def update(self, dt):
        if self.rect:
            self.rect.centerx -= 200 * dt
            if self.rect.right < 0:
                Background(self.groups, self.sprites, (WINDOW_WIDTH/2+180, WINDOW_HEIGHT/2), layer=self._layer)
                self.kill()
                
class Foreground(pygame.sprite.Sprite):
    def __init__(self, groups, layer, image_path, pos):
        self._layer = layer
        super().__init__()
        self.add(groups)
        self.image = image_path
        self.image = pygame.transform.scale(self.image, (400, 50))
        self.rect = self.image.get_frect(midbottom=pos)
    def update(self, dt) -> None:
         if self.rect:
             self.rect.x -= 50 * dt
             if self.rect.right < 0:
                 self.rect.x = 400