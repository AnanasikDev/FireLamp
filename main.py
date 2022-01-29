# SPDX-FileCopyrightText: 2020 Melissa LeBlanc-Williams, written for Adafruit Industries
# SPDX-License-Identifier: MIT
import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer
from time import sleep

pixel_pin = board.GPIO_12
pixel_width = 16
pixel_height = 16

pixels = neopixel.NeoPixel(
    pixel_pin, pixel_width * pixel_height, brightness=0.1, auto_write=False,
)

pixel_framebuf = PixelFramebuffer(pixels, pixel_width, pixel_height, reverse_x=True,)

pixel_framebuf.fill(0x000088)
pixel_framebuf.display()
sleep(2)