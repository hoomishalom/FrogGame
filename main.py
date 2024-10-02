import pygame
from initObjects import *
from os.path import join


pygame.init()
pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1000, 800
TICKS = 60
PLAYER_VEL = 5

run = True
paused = False
offset_x = 0
scroll_area_width = 150
ui_devider = 10

window = pygame.display.set_mode((WIDTH, HEIGHT))
alpha_window = pygame.Surface((WIDTH, HEIGHT))
alpha_window.set_alpha(64)

key_binds = {
    "move_right": pygame.K_d,
    "move_left": pygame.K_a,
    "scroll_right": pygame.K_e,
    "scroll_left": pygame.K_q,
    "pause": pygame.K_p,
    "quit": pygame.K_ESCAPE,
    
    "jump": pygame.K_SPACE,
}


def get_background(name):
    image = pygame.image.load(join("assets", "background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, players, objects, ui_objects, offset_x):
    global paused
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    for player in players:
        player.draw(window, offset_x)
        player.draw_name(window, offset_x)

    for ui_obj in ui_objects:
        if ui_obj.type == "Menu":
            if paused:
                ui_obj.draw(window, offset_x)
        else:
            if ui_obj.type == "Menu":
                ui_obj.draw(window, offset_x)

    if paused:
        window.blit(alpha_window, (0, 0))
    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []

    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.collide_player_top()
                player.landed()
            elif dy < 0:
                player.rect.top = obj.collide_player_bottom()
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_key_press(player, objects):
    global offset_x, run, paused
    keys = pygame.key.get_pressed()
    collide_left = collide(player, objects, int(-PLAYER_VEL * 1.5))
    collide_right = collide(player, objects, int(PLAYER_VEL * 1.5))

    player.x_vel = 0
    if not paused:
        if keys[key_binds["move_left"]]:
            player.direction = "left"
            if not collide_left:
                player.move_left(PLAYER_VEL)

        if keys[key_binds["move_right"]]:
            player.direction = "right"
            if not collide_right:
                player.move_right(PLAYER_VEL)

        if keys[key_binds["scroll_right"]]:
            offset_x += 5
            player.direction = "right"

        if keys[key_binds["scroll_left"]]:
            offset_x -= 5
            player.direction = "left"

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire" and obj.active == True:
            obj.player_hit(player)


def main(window):
    global offset_x, run, paused, scroll_area_width
    clock = pygame.time.Clock()
    background, bg_image = get_background("Green.png")

    while run:
        clock.tick(TICKS)
        fps = int(clock.get_fps())
        display_fps.update(fps)

        # display_position.update(f"{players[0].rect.x} / {players[0].rect.y}")
        display_position.update("%-5.d / %5.d" % (players[0].rect.x, players[0].rect.y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not paused:
                    mpos = pygame.mouse.get_pos()
                    for button in buttons:
                        button.click(mpos)

            for player in players:
                if event.type == pygame.KEYDOWN:
                    if (
                        not paused
                        and event.key is key_binds["jump"]
                        and player.jump_count < 2
                    ):
                        player.jump()

                    if event.key is key_binds["quit"]:
                        run = False

                    if event.key is key_binds["pause"]:
                        paused = not paused
                        for ui in ui_objects:
                            if ui.name == "paused_state":
                                ui.update(paused)

        for player in players:
            player.loop(TICKS)
            if (
                (player.rect.right - offset_x >= WIDTH - scroll_area_width)
                and player.x_vel > 0
            ) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0
            ):
                offset_x += player.x_vel

            handle_key_press(player, objects)

        for obj in objects:
            if obj.name == "fire":
                obj.loop()
        draw(window, background, bg_image, players, objects, ui_objects, offset_x)

    pygame.quit()


if __name__ == "__main__":
    main(window)
