"""
Drawing zero on the screen
"""

import sys

import numpy as np
import sdl2
import sdl2.ext

from sprites import hex_digit_sprites

WHITE_VALUE = 16777215  # 2^24 - 1
WHITE = sdl2.ext.Color(255, 255, 255)


def block_sprite(window):
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    sp_zero = factory.from_color(WHITE, size=(80, 50))

    spriterenderer = factory.create_sprite_render_system(window)
    spriterenderer.render(sp_zero)


def pixel_sprite(window):
    """drawing zero directly without defining sprite like in the standard"""
    # pixels2d returns numpy array
    window_surface = sdl2.ext.pixels2d(window.get_surface())

    window_surface[:80, :10] = WHITE_VALUE
    window_surface[:80, 40:50] = WHITE_VALUE

    window_surface[:20, :50] = WHITE_VALUE
    window_surface[60:80, :50] = WHITE_VALUE


def hex_sprite_to_array(hex_sprite):
    bin_arr = []
    for num in hex_sprite.split():
        bin_num = bin(eval(num))[2:]
        bin_arr.append([int(b) for b in bin_num])
    return np.asarray(bin_arr)


def run():
    pixel_zero = hex_sprite_to_array(hex_digit_sprites.zero)
    pixel_zero_zoomed = np.repeat(pixel_zero, 10, axis=1)  # stretch horizontally
    pixel_zero_zoomed = np.repeat(pixel_zero_zoomed, 10, axis=0)  # stretch vertically
    pixel_vertical, pixel_horizontal = pixel_zero_zoomed.shape

    sdl2.ext.init()
    window = sdl2.ext.Window("chip8 display", size=(640, 320))

    window_surface = sdl2.ext.pixels2d(window.get_surface())
    window_surface[:pixel_vertical, :pixel_horizontal] = pixel_zero_zoomed * WHITE_VALUE

    window.show()

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        window.refresh()

    return 0


if __name__ == "__main__":
    sys.exit(run())
