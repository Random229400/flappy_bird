from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, layer, collide_sprites):
        self._layer = layer
        super().__init__() 
        self.add(groups)

        # Sprite Sheet
        spritesheet = SpriteHelper(join("assets", 'Player', 'StyleBird1', 'Bird1-1.png'))
        raw_frames = [spritesheet.get_frame(i * 16, 0, 16, 16) for i in range(4)]
        self.frames = [pygame.transform.scale(frame, (50, 50)) for frame in raw_frames]
        self.current_frame = 0

        self.original_image = self.frames[self.current_frame]   
        self.image = self.original_image
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH * .2, WINDOW_HEIGHT / 2))
        self.collide_sprite = collide_sprites

        self.animation_speed = .15
        self.animation_timer = 0
        self.flapping = False
        self.flap_frames = len(self.frames)
        self.frames_played = 0

        # stats
        self.live: bool = True
        self.y_velocity = 0
        self.gravity = 750
        self.jump_force = -300
        
    def update(self, dt: float):
        if self.live:
            self.y_velocity += self.gravity * dt
            self.rect.centery += self.y_velocity * dt # type: ignore
            
            # Jump
            if self.rect:
                    if self.rect.top <= -5:
                        self.rect.top = 0
                        self.jump_force = 0
                    else:
                        self.jump_force = -300

            #Animation
            if self.flapping:
                self.animation_timer += dt

                if self.animation_timer >= self.animation_speed:
                    self.animation_timer = 0
                    self.frames_played += 1
                    self.current_frame = (self.current_frame + 1 ) % len(self.frames)
                    self.image = self.frames[self.current_frame]

                    if self.frames_played > self.flap_frames:
                        self.flapping = False
            
            # collision 
            if pygame.sprite.spritecollide(self, self.collide_sprite, dokill=False, collided=pygame.sprite.collide_mask):
                self.live = False