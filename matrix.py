from time import sleep as wait, strftime as time
from random import randint as rand, uniform
from random import choice as choose
from rpi_ws281x import *
import argparse
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from math import log, sin, pi
import matplotlib.colors as colors

#######################################
LED_COUNT = 256  # Суммарное кол-во светодиодов (256 для 16 на 16)
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 15  # Яркость (0 - 255)
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
#######################################
MODE = 2
MODES_Count = 6

_strip = None
_args = None
_pressed = False
modechanged = False
#######################################
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
yellow = [255, 255, 0]
light_blue = [0, 255, 255]
white = [255,255,255]
black = [0, 0, 0]
purple = [255, 0, 255]
orange = [255, 130, 0]


def _normalDistribution(min, max, std_deviation = 2, horizontal_mean = 4.0):
    mean = (min + max) / 2.0 + horizontal_mean
    stdDev = std_deviation
    u1 = 1.0 - uniform(0.0, 0.9999)
    u2 = 1.0 - uniform(0.0, 0.9999)
    randStdNormal = (-2.0 * log(u1) * sin(2.0 * pi * u2)) ** 0.5
    randNormal = mean + stdDev * randStdNormal
    return randNormal.real


def changeMode(channel):
    global MODE, _pressed
    print("Кнопка нажата")
    MODE += 1
    if (MODE > MODES_Count):
        MODE = 1
    _pressed = True
    print(MODE)


def init():
    global _args, _strip
    #####################
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(10, GPIO.RISING, callback=changeMode)  # Setup event on pin 10 rising edge
    #####################
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    _args = parser.parse_args()
    #####################
    # Create NeoPixel object with appropriate configuration.
    _strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    _strip.begin()
    #####################
    print(f"Started at {time('%H:%M:%S')}")


init()


def setPixel(index, color):
    _strip.setPixelColor(index, color)


def update():
    _strip.show()


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


#######################################
### Режимы
### 0 : randomFill - плавное случайное заполнение
### 1 : fill - заполнение случайным цветом
### 2 : fire - огонь
#######################################


def randomFill(massive=300, speed=1.0):
    global _pressed, modechanged
    speed = 1 / speed
    while True:
        for i in range(massive):
            if _pressed or modechanged:
                _pressed = False
                modechanged = False
                return
            setPixel(rand(0, 255), ColorClass.getRandomColor())
            update()
            wait(uniform(0.05 * speed, 0.12 * speed))
        for i in range(massive*3):
            if _pressed or modechanged:
                _pressed = False
                modechanged = False
                return
            setPixel(rand(0, 255), Color(0, 0, 0))
            update()
            wait(uniform(0.004 * speed, 0.01 * speed))


def fill(color=None, delay=1.0):
    # global _pressed
    if color is None : color = ColorClass.getRandomColor(45)
    for j in range(256):
        setPixel(j, color)
    update()
    # for i in range(10):
    #     if not _pressed:
    #         wait(delay/10)


def fire():
    global _pressed, modechanged
    for i in range(rand(250, 650)):
        if _pressed or modechanged:
            _pressed = False
            modechanged = False
            return
        pos = rand(0, 15) * round(_normalDistribution(0, 16, horizontal_mean=uniform(1.2, 3.5)))
        p = Pixel(256 - pos, Color(220, 1 * pos // 3, 0))
        #p.x = round(_normalDistribution(0, 16, horizontal_mean=uniform(-4, 4)))
        p.x = rand(0, 15)
        p.xyToIndex()
        p.draw()
    update()
    for i in range(rand(250, 650)):
        if _pressed or modechanged:
            _pressed = False
            modechanged = False
            return
        pos = rand(0, 15) * round(_normalDistribution(0, 16, horizontal_mean=uniform(1.2, 3.5)))
        p = Pixel(pos, Color(0,0,0))
        p.x = round(_normalDistribution(0, 16, horizontal_mean=uniform(-4, 4)))
        p.xyToIndex()
        p.draw()
    wait(uniform(0.08, 0.13))


def candle():
    # _colors = [Color(108, 39, 0), Color(110, 41, 1), Color(106, 40, 0), Color(107, 37, 0), Color(102, 38, 0),
    #            Color(104, 40, 1), Color(112, 42, 0), Color(110, 40, 1), Color(111, 39, 2), Color(77, 28, 1),
    #            Color(99, 36, 1)]
    # _colors = [Color(100, 40, 0), Color(97, 37, 0), Color(101, 39, 0), Color(102, 41, 0),
    #            Color(99, 39, 1), Color(103, 43, 1), Color(102, 36, 0), Color(109, 45, 0),
    #            Color()]
    _colors = [Color(108, 39, 0), Color(110, 41, 1), Color(106, 40, 0), Color(107, 37, 0), Color(102, 38, 0),
               Color(104, 40, 1), Color(109, 42, 0), Color(110, 40, 1), Color(108, 39, 2), Color(92, 36, 1),
               Color(99, 36, 1)]
    fill(choose(_colors), 0)
    wait(uniform(0.085, 0.25))


# def rainbow():
#     colors = [red, orange, yellow, green]
#     color = ColorClass.rgb_to_hex(red)
#     while True:
#         print(color)
#         color = ColorClass.changeColor(color, orange)  # colors[colors.index(color) + 1]
#         print(color)
#         if _pressed:
#             return
#         fill(Color(color[0], color[1], color[2]), 0)
#         wait(0.1)

class Drop:
    def __init__(self, length, color, x, y, bgc):
        self.len = length
        self.color = color
        self.x = x
        self.y = y
        self.index = x + y*16
        self.parts = list([self.index + i*16 for i in range(1, self.len+1)])
        self.bgc = bgc #ColorClass.modificateColor(self.color, -10, 10)
        fill(self.bgc, 0)

    def draw(self):
        for drop in self.parts:
            if drop >= 0:
                setPixel(drop, Color(self.color[0], self.color[1], self.color[2]))

    def move(self, x, y):
        self.index += y * rand(8, 15) + x
        self.index %= 255
        self.index = abs(self.index)

        self.parts.append(self.index)
        setPixel(self.parts[0], self.bgc)
        self.parts.remove(self.parts[0])
        print(self.parts)


def rain():
    global _pressed, modechanged
    count = 6
    drops = []
    for i in range(count):
        drops.append(Drop(7 + rand(-2, 3), [0, 105 + rand(-10, 10), 225 + rand(-5, 4)], rand(0, 15), rand(-2, 0),
                          ColorClass.modificateColor([6, 30 + rand(-5, 5), 30 + rand(-2, 3)])))
    print("ИНИЦИАЛИ")
    while True:
        if _pressed or modechanged:
            _pressed = False
            modechanged = False
            return
        for d in drops:
            d.move(0, 1)
            d.draw()
        update()
        wait(uniform(0.05, 0.15))


def lava():
    global _pressed, modechanged
    count = 6
    drops = []
    for i in range(count):
        drops.append(Drop(10 + rand(-2, 3), [75, 110 + rand(-5, 5), 10 + rand(-5, 4)], rand(0, 15), rand(6, 13),
                          ColorClass.modificateColor([250, 14, 6])))
    print("ИНИЦИАЛИ")
    while True:
        if _pressed or modechanged:
            _pressed = False
            modechanged = False
            return
        for d in drops:
            d.move(0, -1)
            d.draw()
        update()
        wait(uniform(0.05, 0.15))


def rainbow():
    for i in range(255-16, 255):
        setPixel(i, Color(255, 0, 0))
    for i in range(255-48, 255-32):
        setPixel(i, Color(255, 128, 0))
    for i in range(255-80, 255-64):
        setPixel(i, Color(255, 255, 0))
    for i in range(255-112, 255-96):
        setPixel(i, Color(0, 255, 0))
    for i in range(255-144, 255-128):
        setPixel(i, Color(100, 100, 255))
    for i in range(255-176, 255-160):
        setPixel(i, Color(0, 0, 255))
    for i in range(255-202, 255-192):
        setPixel(i, Color(255, 0, 255))
    update()


modes = {1: randomFill,
          2: fire,
          3: candle,
          4: rain,
          5: lava,
          6: rainbow}


def process_mode():
    while True:
        if 1 <= MODE <= 6:
            print(MODE)
            modes[MODE]()


# while True:
#     if _pressed:
#         fill(Color(0, 0, 0), 0)
#         _pressed = False
#     _modes[MODE]()
# 120 яркость белый цвет на всю матрицу 2 А