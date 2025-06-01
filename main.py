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
        self.start = False

        # Load assets
        self.background_sprites = [
            pygame.image.load(join('assets', 'Background', f'Background{bg}.png')).convert_alpha()
            for bg in range(3, 6)
        ]
        foreground_path = pygame.image.load(join('assets', 'assets', 'ground.png')).convert()
        pipe_up_path = pygame.image.load(join('assets', 'assets', 'pipe_up.png')).convert_alpha()
        pipe_down_path = pygame.image.load(join('assets', 'assets', 'pipe_down.png')).convert_alpha()

        # Text helpers (refactored: use consistent positions)
        self.title_text = TextHelper('Flappy Bird', 'white', 80, (WINDOW_WIDTH // 2, 100))
        self.play_button = TextHelper('Play', 'black', 50, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        self.score_text = TextHelper(0, 'gray', 75, (WINDOW_WIDTH // 2, 75))
        self.over_text = TextHelper('Game Over!', 'red', 90, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.bottom_text = TextHelper('Press r to restart', 'red', 35, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        self.take_menu_text = TextHelper('Press e to return home', 'red', 35, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.high_score_text = TextHelper('High Score:', 'gray', 30, (75, 25))
        self.high_score = TextHelper(0, 'gray', 30, (150, 25))

        # Sprite groups and layers
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.collide_sprite = pygame.sprite.Group()
        BACKGROUND_LAYER = 0
        FOREGROUND_LAYER = 3
        PIPE_LAYER = 1
        PLAYER_LAYER = 2

        # Sprites
        self.player = Player(self.all_sprites, layer=PLAYER_LAYER, collide_sprites=self.collide_sprite)
        Background(self.all_sprites, self.background_sprites, (0, WINDOW_HEIGHT / 2), layer=BACKGROUND_LAYER)
        Background(self.all_sprites, self.background_sprites, (WINDOW_WIDTH, WINDOW_HEIGHT / 2), layer=BACKGROUND_LAYER)
        Foreground((self.all_sprites, self.collide_sprite), FOREGROUND_LAYER, foreground_path, (WINDOW_WIDTH / 2, WINDOW_HEIGHT))
        Foreground((self.all_sprites, self.collide_sprite), FOREGROUND_LAYER, foreground_path, (WINDOW_WIDTH + 200, WINDOW_HEIGHT))
        self.pipe = PipeUp((self.all_sprites, self.collide_sprite), layer=PIPE_LAYER, image_path=pipe_down_path, other_path=pipe_up_path, collide_sprite=self.player)

    def score(self):
        if self.player.rect and self.pipe.rect:
            if self.player.live and self.player.rect.centerx > self.pipe.rect.centerx and self.can_score:
                self.points += 1
                self.can_score = False
                self.score_text.set_score(self.points)
                self.pipe.speed += 5
                self.pipe.gap -= 0.075
            elif self.pipe.rect.right > 400:
                self.can_score = True

    def reset_game(self):
        self.pipe.reset()
        self.points = 0
        self.can_score = True
        self.score_text.set_score(self.points)
        if self.player.rect:
            self.player.rect.center = (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 2)
        self.player.y_velocity = 0
        self.player.live = True
        self.player.flapping = False
        self.player.current_frame = 0
        self.player.animation_timer = 0
        self.player.frames_played = 0
        self.player.image = self.player.frames[self.player.current_frame]
        self.start = True

    async def run(self):
        while self.running:
            await asyncio.sleep(0)
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.player.live and self.start:
                        self.player.y_velocity = self.player.jump_force
                        self.player.flapping = True
                        self.player.current_frame = 0
                        self.player.animation_timer = 0
                        self.player.frames_played = 0
                        self.player.image = self.player.frames[self.player.current_frame]
                    if not self.player.live and event.key == pygame.K_r:
                        self.reset_game()
                    if not self.player.live and event.key == pygame.K_e:
                        self.start = False
                        self.player.live = True
                        if self.player.rect:
                            self.player.rect.centery = WINDOW_HEIGHT / 2
            self.screen.fill('black')
            self.all_sprites.draw(self.screen)
            self.high_score_text.render(self.screen)
            self.high_score.render(self.screen)
            if self.player.live:
                if self.start:
                    self.score_text.render(self.screen)
                    self.all_sprites.update(dt)
                    if self.score_text.text_value > self.high_score.text_value:
                        self.high_score.set_score(self.score_text.text_value)
                    self.score()
                else:
                    if self.player.rect:
                        self.player.rect.centerx = WINDOW_WIDTH/2
                    self.player.start_anim(dt)
                    self.title_text.render(self.screen)
                    self.play_button.render(self.screen)
                    pygame.draw.rect(self.screen, 'black', self.play_button.rect.inflate(20, 20), 5, 1)
                    if pygame.FRect.collidepoint(self.play_button.rect.inflate(20, 20), pygame.mouse.get_pos()):
                        self.play_button.color = 'gray'
                        if pygame.mouse.get_just_pressed()[0]:
                            self.reset_game()
                    else:
                        self.play_button.color = 'black'
            else:
                if self.score_text.text_value > self.high_score.text_value:
                    self.high_score.set_score(self.score_text.text_value)
                self.over_text.render(self.screen)
                self.bottom_text.render(self.screen)
                self.take_menu_text.render(self.screen)
            pygame.display.update()
        pygame.quit()

async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())