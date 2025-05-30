from settings import *
from player import Player
from background import *
from pipe import *

class Game:
    def __init__(self):
        # General Setup
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.running = True
        self.points = 0
        self.can_score = True
        
        # Imports
        self.background_sprites: list = []
        for background in range(3, 6):
            image_path = join('assets', 'Background', 'Background' + str(background) + '.png')
            image = pygame.image.load(image_path).convert_alpha()
            self.background_sprites.append(image)
        
        foreground_path = pygame.image.load(join('assets', 'assets', 'ground.png')).convert()
        pipe_up_path = pygame.image.load(join('assets', 'assets', 'pipe_up.png')).convert_alpha()
        pipe_down_path = pygame.image.load(join('assets', 'assets', 'pipe_down.png')).convert_alpha()
        self.text = TextHelper(0, 'gray', 75)
        

        # Sprites
        self.all_sprites: pygame.sprite.LayeredUpdates = pygame.sprite.LayeredUpdates()
        self.collide_sprite: pygame.sprite.Group = pygame.sprite.Group()
        BACKGROUND_LAYER = 0
        FOREGROUND_LAYER = 3
        PIPE_LAYER = 1
        PLAYER_LAYER = 2
        
        self.player = Player(self.all_sprites, layer=PLAYER_LAYER, collide_sprites=self.collide_sprite)
        Background(self.all_sprites, self.background_sprites, (0, WINDOW_HEIGHT/2), layer=BACKGROUND_LAYER)
        Background((self.all_sprites), self.background_sprites, (WINDOW_WIDTH, WINDOW_HEIGHT/2), layer=BACKGROUND_LAYER)
        Foreground((self.all_sprites, self.collide_sprite), FOREGROUND_LAYER, foreground_path, (WINDOW_WIDTH/2, WINDOW_HEIGHT))
        Foreground((self.all_sprites, self.collide_sprite), FOREGROUND_LAYER, foreground_path, (WINDOW_WIDTH+200, WINDOW_HEIGHT))
        self.pipe = PipeUp((self.all_sprites, self.collide_sprite), layer=PIPE_LAYER, image_path=pipe_down_path, other_path=pipe_up_path, collide_sprite=self.player)
    
    def score(self):
        if self.player.rect and self.pipe.rect:
            if self.player.live and self.player.rect.centerx > self.pipe.rect.centerx and self.can_score:
                self.points += 1
                self.can_score = False
                self.text.set_score(self.points)
                self.pipe.speed += 5
                self.pipe.gap -= .075
            elif self.pipe.rect.right > 400:
                self.can_score = True
    
    def game_over(self):
        text = TextHelper('Game Over', 'black', 100)
        
    async def run(self):
        while self.running:
            await asyncio.sleep(0)
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.y_velocity = self.player.jump_force
                        self.player.flapping = True
                        self.player.current_frame = 0
                        self.player.animation_timer = 0
                        self.player.frames_played = 0
                        self.player.image = self.player.frames[self.player.current_frame]
            if self.player.live:
                self.screen.fill('black')
                self.all_sprites.draw(self.screen)
                self.all_sprites.update(dt)
                self.score()
                self.text.render(self.screen, (WINDOW_WIDTH / 2, 75))
                pygame.display.update() # type: ignore
            else:
                return
        pygame.quit()

async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())