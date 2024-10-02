import pygame
import loaderFunc


class Player(pygame.sprite.Sprite):
    pygame.font.init()
    MAIN_FONT = pygame.font.SysFont("Comic Sans MS", 24)
    COLOR = (255, 0, 0)
    GRAVITY = 0.7
    SPRITES = loaderFunc.load_sprite_sheets(
        "MainCharacters", "NinjaFrog", 32, 32, 2, True
    )
    ANIMATION_DELAY = 4
    JUMP_HEIGHT = 8

    def __init__(self, x, y, width, height, name):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.name = name
        self.mask = None
        self.direction = "right"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    def jump(self):
        self.y_vel = -self.JUMP_HEIGHT
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, mx=0, my=0):
        self.rect.x += mx
        self.rect.y += my

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, FPS):
        self.y_vel += min(1, (self.fall_count / FPS) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > FPS * 1.5:
            self.hit = False

        self.update_sprite()
        self.fall_count += 1

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 3:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw_name(self, window, offset_x):
        self.name_tag = self.MAIN_FONT.render(self.name, False, (0, 0, 0))
        self.name_loc = (
            self.rect.topleft[0] - offset_x - 20,
            self.rect.topleft[1] - 30,
        )

        window.blit(self.name_tag, self.name_loc)

    def draw(self, window, offset_x):
        window.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
