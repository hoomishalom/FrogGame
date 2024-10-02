import pygame
import loaderFunc


class uiObject:
    pygame.font.init()

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        name: str,
        scale: int,
        text: str = None,
        bg_color: tuple[int, int, int] = None,
        sprite_loc: tuple[str, str] = None,
        func=None,
        type=None,
    ):
        self.MAIN_FONT = pygame.font.SysFont("Minecraft", int(24 * scale))
        self.sprites = None
        self.button = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.scale = scale

        if func:
            self.click_func = func
            self.type = "button"

        if not text:
            self.sprite_loc = sprite_loc
            self.sprites = loaderFunc.load_sprite_sheets(
                *sprite_loc, width, height, self.scale
            )
            self.rect = pygame.Rect(
                self.x, self.y, self.width * self.scale, int(self.height * self.scale)
            )
        else:
            self.bg_color = bg_color
            self.text = text

            if self.bg_color:
                self.button = self.MAIN_FONT.render(
                    self.text, False, (0, 0, 0)
                    # , self.bg_color
                )
            else:
                self.button = self.MAIN_FONT.render(self.text, False, (0, 0, 0))

            self.rect = self.button.get_rect()
            self.rect.topleft = (self.x, self.y)

    def click(self, mpos):
        if self.rect.collidepoint(mpos):
            print("collided", self.name)
            self.click_func()

    def draw(self, window, offset_x=0):
        if self.sprites:
            window.blit(self.sprites["toggle"][0], (self.rect.x, self.rect.y))
        elif self.type == "button":
            window.blit(self.button, (self.rect.x, self.rect.y))
        elif self.type == "updated_text":
            window.blit(self.display_text, (self.rect.x, self.rect.y))
