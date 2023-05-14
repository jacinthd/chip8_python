"""
Drawing all hex sprites on the screen
Refer https://multigesture.net/articles/how-to-write-an-emulator-chip-8-interpreter/
Keypad test application using inbuilt fonts
"""

import sys

import numpy as np
import sdl2
import sdl2.ext

from sprites.fontset import chip8_fontset

WHITE_VALUE = 16777215  # 2^24 - 1


def hex_sprite_to_array(hex_sprite):
    bin_arr = []
    for num in hex_sprite:
        bin_num = bin(eval(num))[2:]
        if len(bin_num) < 8:
            zero_padding = '0' * (8 - len(bin_num))
            bin_num = f"{zero_padding}{bin_num}"
        bin_arr.append([int(b) for b in bin_num])
    return np.asarray(bin_arr)


def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("chip8 display", size=(640, 320))
    window_surface = sdl2.ext.pixels2d(window.get_surface(), transpose=False)

    y_ptr, x_ptr = 10, 10
    for i, font in enumerate(chip8_fontset):
        pixel_sprite = hex_sprite_to_array(font)
        pixel_sprite_zoomed = np.repeat(pixel_sprite, 10, axis=1)  # stretch horizontally
        pixel_sprite_zoomed = np.repeat(pixel_sprite_zoomed, 10, axis=0)  # stretch vertically
        y, x = pixel_sprite_zoomed.shape
        window_surface[y_ptr:y_ptr + y, x_ptr:x_ptr + x] = pixel_sprite_zoomed * WHITE_VALUE
        if i == 0 or i % 4 != 3:
            x_ptr += x
        else:
            y_ptr += 30 + y
            x_ptr = 10

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
