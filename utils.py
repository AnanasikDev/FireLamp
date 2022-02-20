# from math import log2, log, pi, sin
# from random import uniform
from rpi_ws281x import *
from modes import *
import argparse
# import RPi.GPIO as GPIO
from matrix import *

# MODES CLASSES


class Pixel:
    def __init__(self, index, color):
        self.index = index
        self.color = color

        self.x = index % 16
        self.y = index // 16

        self._previous_index = self.index

    def move(self, x, y):
        self._previous_index = self.index
        self.index += x + y * 16

    def moveAt(self, newx, newy):
        self._previous_index = self.index
        setPixel(self._previous_index, Color(0, 0, 0))
        self.x = newx
        self.y = newy

    def draw(self):
        setPixel(self._previous_index, Color(0, 0, 0))
        setPixel(self.index, self.color)
        pass

    def xyToIndex(self):
        self.index = self.x + self.y * 16


class ColorClass:
    @staticmethod
    def getRandomColor(_min=0, _max=255):
        return Color(rand(_min, _max), rand(_min, _max), rand(_min, _max))

    @staticmethod
    def modificateColor(color, min = -5, max = 5):
        return Color(color[0] + rand(min, max), color[1] + rand(min, max), color[2] + rand(min, max))

    @staticmethod
    def changeColor(color, new_color):  # color - hex, new_color - rgb
        color = ColorClass.hex_to_rgb(color)

        r = (color[0] - new_color[0]) // 2
        g = (color[1] - new_color[1]) // 2
        b = (color[2] - new_color[2]) // 2

        color[0] += r
        color[1] += g
        color[2] += b

        color[0] = abs(color[0])
        color[1] = abs(color[1])
        color[2] = abs(color[2])
        # print(color)
        return color  #ColorClass.rgb_to_hex(color)

    @staticmethod
    def hex_to_rgb(hex_string):
        rgb = colors.hex2color(hex_string)
        #return list([int(255 * x) for x in rgb])
        print(f"hex to rgb. RGB value is {rgb}")
        return list([int(1.0 * x) for x in rgb])

    @staticmethod
    def rgb_to_hex(rgb_tuple):
        return colors.rgb2hex([1.0 * x / 255 for x in rgb_tuple])

    @staticmethod
    def lerp(origin_color, target_color, k):
        new_color = Color(origin_color.r, origin_color.g, origin_color.b);
        new_color.r += (target_color.r - origin_color.r) * k
        new_color.g += (target_color.g - origin_color.g) * k
        new_color.b += (target_color.b - origin_color.b) * k

        return new_color


# MATH


def clamp(value, minv, maxv):
    return max(min(value, maxv), minv)


def lerp_num(a, b, t):
    return a + t * (b - a)


def repeat(value, min, max):
    if value > max:
        value = min
    elif value < min:
        value = max
    return value


def normalDistribution(min, max, std_deviation = 2, horizontal_mean = 4.0):
    mean = (min + max) / 2.0 + horizontal_mean
    stdDev = std_deviation
    u1 = 1.0 - uniform(0.0, 0.9999)
    u2 = 1.0 - uniform(0.0, 0.9999)
    randStdNormal = (-2.0 * log(u1) * sin(2.0 * pi * u2)) ** 0.5
    randNormal = mean + stdDev * randStdNormal
    return randNormal.real


def bounds(n, a, b):
    return a <= b <= b


# COLORS


def clamp_color(color):
    if color[0] < 0:
        color[0] = 0
    if color[1] < 0:
        color[1] = 0
    if color[2] < 0:
        color[2] = 0

    if color[0] > 255:
        color[0] = 255
    if color[1] > 255:
        color[1] = 255
    if color[2] > 255:
        color[2] = 255


def lerp_color(color, target_color, t):
    return [lerp_num(color[0], target_color[0], t),
            lerp_num(color[1], target_color[1], t),
            lerp_num(color[2], target_color[2], t)]


def shift_hue(color, shift):
    # 0.00 - 0.33 = красный - зеленый
    # 0.33 - 0.66 = зеленый - синий
    # 0.66 - 0.99 - синий - красный

    shift = repeat(shift, 0.0, 1.0)

    contrast = 1.3
    depth = 0.55

    if 0.0 <= shift <= 0.333:
        color[0] = clamp(int(color[0] ** contrast), 0, 255)
        color[1] = clamp(int(color[1] ** depth), 0, 255)
        color[2] = clamp(int(color[2] ** depth), 0, 255)
    if 0.334 <= shift <= 0.666:
        color[0] = clamp(int(color[0] ** depth), 0, 255)
        color[1] = clamp(int(color[1] ** contrast), 0, 255)
        color[2] = clamp(int(color[2] ** depth), 0, 255)
    if 0.667 <= shift <= 1.0:
        color[0] = clamp(int(color[0] ** depth), 0, 255)
        color[1] = clamp(int(color[1] ** depth), 0, 255)
        color[2] = clamp(int(color[2] ** contrast), 0, 255)

    return color


def edit_color(color, func):
    return [func(color[0]), func(color[1]), func(color[2])]


def make_contrast(value):
    if value < 0.1:
        value = value ** 0.5
    else:
        value = value ** 2

    value **= 0.9

    return 255.0 / (value + 1.0) * 100


def fix_color(color):
    color = edit_color(color, lambda light: abs(int(log2(abs(light + 1)))) * 6)
    color = edit_color(color, lambda light : make_contrast(light))
    return color
