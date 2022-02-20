# from time import sleep as wait, strftime as time, time as timesecs
# rom random import randint as rand, uniform
# from random import choice as choose
from rpi_ws281x import *
# import argparse
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
# from math import log, sin, pi, log2
# import matplotlib.colors as colors
# import web
# from utils import *


LED_COUNT = 256  # Суммарное кол-во светодиодов (256 для 16 на 16)
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 70  # Яркость (0 - 255)
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
#######################################
modeS_Count = 7
modeS_ARGS = []

brightness = 1.0

strip = None
_args = None


def setPixel(index, color):
    # r, g, b = color % 256 # ну ты понял (для настройки яркости, контрастности и т.п.)
    b = int(color % 256 * brightness)
    g = int((color // 256) % 256 * brightness)
    r = int((color // 256) // 256 * brightness)

    # g = int(g / 1.2)
    # r = int(r / 1.2)

    c = Color(r, g, b)

    # print(brightness)

    strip.setPixelColor(index, c)


def update():
    strip.show()


def fill(color=None, delay=1.0):
    # global _pressed
    # if color is None : color = ColorClass.getRandomColor(45)
    for j in range(256):
        setPixel(j, color)
    update()
    # for i in range(10):
    #     if not _pressed:
    #         wait(delay/10)


from modes import *


def init():
    global _args, strip
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
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    #####################
    print(f"Started at {time('%H:%M:%S')}")


init()

modeslist = {
          1: randomFill,
          2: fire,
          3: candle,
          4: rain,
          5: lava,
          6: murling,
          7: shimmer}


def process_mode():
    while True:
        if 1 <= mode <= len(modeslist):
            # print(mode) # debug
            modeslist[mode](modeS_ARGS)


# while True:
#     if pressed:
#         fill(Color(0, 0, 0), 0)
#         pressed = False
#     _modes[mode]()
# 120 яркость белый цвет на всю матрицу 2 А