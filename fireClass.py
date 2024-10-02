import pygame, loaderFunc, objectClass


class Fire(objectClass.Object):
    ANIMATION_DELAY = 3
    name = "fire"

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        self.fire_rect = pygame.Rect(x, y - height, width, height)
        self.collided_rect = pygame.Rect(x, y, width, height)

        self.sprite_sheet = loaderFunc.load_sprite_sheets(
            "Traps", "Fire", width, height, 2
        )
        self.image = self.sprite_sheet["off"][0]

        self.mask = pygame.mask.from_surface(self.image)

        self.animation_count = 0
        self.animation_name = "off"
        self.active = False

    def on(self):
        self.active = True
        self.animation_name = "on"

    def off(self):
        self.active = False
        self.animation_name = "off"

    def cycle(self):
        self.active = not self.active

        if self.active:
            self.on()
        else:
            self.off()

    def draw(self, window, offset_x=None):
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y))

    def loop(self):
        sprites = self.sprite_sheet[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)

        self.image = sprites[sprite_index]
        self.animation_count += 1

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

    def collide_player_top(self):
        return self.collided_rect.top + (self.collided_rect.height)

    def player_hit(self, player):
        if pygame.Rect.colliderect(self.fire_rect, player.rect):
            player.make_hit()
