import uiClass, buttonClass, fireClass, blockClass, playerClass, updatedTextClass
from main import HEIGHT, WIDTH, paused, ui_devider

block_size = 96

players = [playerClass.Player(100, 100, 50, 50, "HostPlayer")]
fire = fireClass.Fire(block_size * 3, HEIGHT - block_size - 64, 16, 32)
floor = [
    blockClass.Block(i * block_size, HEIGHT - block_size, block_size)
    for i in range(-WIDTH // block_size, (WIDTH * 4) // block_size)
]
blocks = [
    blockClass.Block(block_size * 2, HEIGHT - block_size * 4, block_size),
    blockClass.Block(0, HEIGHT - block_size * 2, block_size),
]

toggle_fire = buttonClass.Button(
    10,
    ui_devider,
    0,
    0,
    "ToggleFireTrap",
    fire.cycle,
    "On/Off",
    "Toggle",
    (125, 125, 125),
    1.5,
)


def cyclePause():
    global paused
    print(paused, "cycle")
    paused = not paused


resume = buttonClass.Button(
    0,
    0,
    0,
    0,
    "ResumeGame",
    cyclePause,
    "Resume",
    "Menu",
    (125, 125, 125),
    1.5,
    middle_top=(WIDTH / 2, ui_devider + 200),
)

paused_state = updatedTextClass.updatedTextObject(
    10, ui_devider + 50, "paused_state", 1.5, "Pause", (125, 125, 125), str(paused)
)
display_fps = updatedTextClass.updatedTextObject(
    10, ui_devider + 100, "fps", 1.5, "FPS", (125, 125, 125)
)
display_position = updatedTextClass.updatedTextObject(10, ui_devider + 150, "position", 1.5, "X/Y", (125,125,125), f"{players[0].rect.x} / {players[0].rect.y}")


buttons = [toggle_fire]
ui_objects = [*buttons, paused_state, display_fps, display_position]
objects = [
    fire,
    *floor,
    *blocks,
]
menu = [resume]
