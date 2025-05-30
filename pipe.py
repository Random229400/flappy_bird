from settings import *

class PipeUp(pygame.sprite.Sprite):
    def __init__(self, groups, layer, image_path, other_path, collide_sprite):
        self._layer = layer
        super().__init__()
        self.add(groups)
        self.groups = groups
        
        self.image = image_path
        self.y = randint(75, WINDOW_HEIGHT-250)
        self.rect = self.image.get_frect(midbottom=(600, self.y))
        
        self.down_pipe = other_path
        self.player = collide_sprite
        self.gap: float = 135
        self.speed = 250
        PipeDown(self.groups, self._layer, self.down_pipe, self)
    
    def update(self, dt):
        if self.rect:
            self.rect.x -= self.speed * dt
            if self.rect.right < 0:
                self.rect.centerx = 500
                self.rect.bottom = randint(75, WINDOW_HEIGHT-250)
    
class PipeDown(pygame.sprite.Sprite):
    def __init__(self, groups, layer, image_path, pipe_up):
        self._layer = layer
        super().__init__()
        self.add(groups)

        self.pipe = pipe_up
        self.image = image_path
        self.rect = self.image.get_frect(midtop=(600, self.pipe.rect.bottom+self.pipe.gap))
    
    def update(self, dt):
        if self.rect:
            self.rect.x -= self.pipe.speed * dt
            if self.rect.right < 0:
                self.rect.centerx = 500
                self.rect.top = self.pipe.rect.bottom + self.pipe.gap
