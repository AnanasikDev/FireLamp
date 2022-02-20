from time import sleep as wait, strftime as time, time as timesecs
from random import randint as rand, uniform
from random import choice as choose
# from rpi_ws281x import *
# import argparse
# import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from math import log, sin, pi, log2
# import matplotlib.colors as colors
# import web
from utils import *
from matrix import *

#######################################
### Режимы
### 0 : randomFill - плавное случайное заполнение
### 1 : fill - заполнение случайным цветом
### 2 : fire - огонь
### TODO:
### Переливание (полное, снизу вверх/сверху вниз)
###
#######################################

mode = 2
pressed = False
modechanged = False


def changeMode(channel):
    global mode, pressed

    print("Кнопка нажата")

    mode = repeat(mode + 1, 1, modeS_Count)

    # mode += 1
    # if mode > modeS_Count:
    #     mode = 1
    pressed = True
    #print(mode)


def randomFill(args):
    global pressed, modechanged

    massive = int(args[1])
    speed = float(args[0])

    while True:
        for i in range(massive):
            if pressed or modechanged:
                pressed = False
                modechanged = False
                return
            setPixel(rand(0, 255), ColorClass.getRandomColor())
            update()
            wait(uniform(0.05, 0.12) / speed)
        for i in range(massive*3):
            if pressed or modechanged:
                pressed = False
                modechanged = False
                return
            setPixel(rand(0, 255), Color(0, 0, 0))
            update()
            wait(uniform(0.004, 0.01) / speed)


# for i in range(100):
#     # if not sunriseon:
#     #     sunriseon = True
#     #     return
#     color = Color(0, 0, i)
#     print(color, i)
#     fill(color)
#     update()
#     wait(0.5)


def fire(args):
    global pressed, modechanged

    if len(args) == 0:
        speed = 1
        freq = 1
    else:
        speed = int(args[0])
        freq = int(args[1])

    for i in range((rand(250, 650) // 4) * clamp(round(log2(freq / 1.2)), 1, 8)):
        if pressed or modechanged:
            pressed = False
            modechanged = False
            return
        pos = rand(0, 15) * round(normalDistribution(0, 16, horizontal_mean=uniform(1.2, 3.5)))
        line = (pos // 16)
        # p = Pixel(256 - pos, Color(220 // 2, 1 * pos // 3, 0))
        # p = Pixel(256 - pos, Color(int(7 * (pos+7)), int(50 // ((pos + 1) / 3)), 0))
        # p = Pixel(256 - pos, Color((10 * pos + 35) * 2, (10 * pos + 35) // 2, 0))
        r = 210 - int(((15 - line)**1.1).real) * 3
        g = clamp(52 + (15 - line) * 12, 10, 95)
        if 16 - line > 13:
            g += (16 - line) * 2
        p = Pixel(256 - pos, Color(r, g, 0))
        print(pos, p.y, line, r, g)
        #p.x = round(_normalDistribution(0, 16, horizontal_mean=uniform(-4, 4)))
        p.x = rand(0, 15)
        p.xyToIndex()
        p.draw()
    update()
    for i in range(rand(250, 650)):
        if pressed or modechanged:
            pressed = False
            modechanged = False
            return
        pos = rand(0, 15) * round(normalDistribution(0, 16, horizontal_mean=uniform(1.2, 3.5)))
        p = Pixel(pos, Color(0,0,0))
        p.x = round(normalDistribution(0, 16, horizontal_mean=uniform(-4, 4)))
        p.xyToIndex()
        p.draw()

    w = (log2(speed+1)/3 - 0.2)
    print(w)

    wait(uniform(0.09, 0.11) / w)
    #wait(0.01)


def candle(args):
    # _colors = [Color(108, 39, 0), Color(110, 41, 1), Color(106, 40, 0), Color(107, 37, 0), Color(102, 38, 0),
    #            Color(104, 40, 1), Color(112, 42, 0), Color(110, 40, 1), Color(111, 39, 2), Color(77, 28, 1),
    #            Color(99, 36, 1)]
    # _colors = [Color(100, 40, 0), Color(97, 37, 0), Color(101, 39, 0), Color(102, 41, 0),
    #            Color(99, 39, 1), Color(103, 43, 1), Color(102, 36, 0), Color(109, 45, 0),
    #            Color()]
    # _colors = [Color(108, 39, 0), Color(110, 41, 1), Color(106, 40, 0), Color(107, 37, 0), Color(102, 38, 0),
    #            Color(104, 40, 1), Color(109, 42, 0), Color(110, 40, 1), Color(108, 39, 2), Color(92, 36, 1),
    #            Color(99, 36, 1)]

    if len(args) == 0:
        speed = 1
    else:
        speed = abs(log2((float(args[0])) / 2.5) / 2.0 + 0.1)

    print(speed)

    # fill(choose(Color(70 + rand(-22, 22), 32 + rand(-9, 9), rand(0, 2))), 0)
    fill(Color(70 + rand(-4, 4), 32 + rand(-7, 7), rand(0, 5)), 0)
    wait(uniform(0.085, 0.25) / speed)


# def rainbow():
#     colors = [red, orange, yellow, green]
#     color = ColorClass.rgb_to_hex(red)
#     while True:
#         print(color)
#         color = ColorClass.changeColor(color, orange)  # colors[colors.index(color) + 1]
#         print(color)
#         if pressed:
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
        # print(self.parts)


def rain(args):
    global pressed, modechanged
    count = 6
    drops = []
    for i in range(count):
        drops.append(Drop(7 + rand(-2, 3), [0, 105 + rand(-10, 10), 225 + rand(-5, 4)], rand(0, 15), rand(-2, 0),
                          ColorClass.modificateColor([6, 30 + rand(-5, 5), 30 + rand(-2, 3)])))
    # print("ИНИЦИАЛИ")
    while True:
        if pressed or modechanged:
            pressed = False
            modechanged = False
            return
        for d in drops:
            d.move(0, 1)
            d.draw()
        update()
        wait(uniform(0.05, 0.15))


def lava(args):
    global pressed, modechanged
    count = 6
    drops = []
    for i in range(count):
        drops.append(Drop(10 + rand(-2, 3), [75, 110 + rand(-5, 5), 10 + rand(-5, 4)], rand(0, 15), rand(6, 13),
                          ColorClass.modificateColor([250, 14, 6])))
    while True:
        if pressed or modechanged:
            pressed = False
            modechanged = False
            return
        for d in drops:
            d.move(0, -1)
            d.draw()
        update()
        wait(uniform(0.05, 0.15))


def rainbow(args):
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
    fill(Color(0,0,0))


def shimmer(args):
    global pressed, modechanged

    color = [0, 200, 0]
    time_step = 0.25
    color_step = 5
    cycles = 40

    for i in range(40): # от зеленого к синему
        color[0] -= 4
        color[1] -= 4
        color[2] += 5
        clamp_color(color)

        # print("зеленый - синий", color)

        for line in range(16):
        #     color[0] -= 1
        #     color[1] -= 1
            for pixel in range(16):
                setPixel(line * 16 + pixel, Color(abs(color[0]), abs(color[1]) // 5, abs(color[2])))
        # fill(Color(abs(color[0]), abs(color[1]) // 5, abs(color[2])))

            # for pixel in range(0 + line % 2, 16, 2):
            #    setPixel(line * 16 + pixel, Color(abs(color[0]), abs(color[1]) // 5, abs(color[2])))

        if pressed or modechanged:
            pressed = False
            modechanged = False
            return

        update()
        wait(0.012)

    wait(0.1)

    for i in range(40): # от синего к красному
        color[0] += 4
        color[1] -= 4
        color[2] -= 5
        clamp_color(color)

        # print("синий - зеленый", color)

        for line in range(16):
            # color[0] -= 1
            # color[1] -= 1

        # fill(Color(abs(color[0]), abs(color[1]) // 5, abs(color[2])))

            # for pixel in range(0 + line % 2 + i % 2, 16, 2):
            #    setPixel(line * 16 + pixel, Color(abs(color[0]), abs(color[1]) // 5, abs(color[2])))
            for pixel in range(16):
                setPixel(line * 16 + pixel, Color(abs(color[0]), abs(color[1]) // 5, abs(color[2])))

        if pressed or modechanged:
            pressed = False
            modechanged = False
            return

        update()
        wait(0.01)

    wait(0.08)

    for i in range(40): # от красного к зеленому
        color[0] -= 4
        color[1] += 4
        color[2] -= 5
        clamp_color(color)

        # print("красный - зеленый", color)

        for line in range(16):
            # color[0] -= 1
            # color[1] -= 1

        # fill(Color(abs(color[0]), abs(color[1]) // 5, abs(color[2])))

            # for pixel in range(0 + line % 2 + i % 2, 16, 2):
            #    setPixel(line * 16 + pixel, Color(abs(color[0]), abs(color[1]) // 5, abs(color[2])))
            for pixel in range(16):
                setPixel(line * 16 + pixel, Color(abs(color[0]), abs(color[1]) // 5, abs(color[2])))

        if pressed or modechanged:
            pressed = False
            modechanged = False
            return

        update()
        wait(0.01)

    wait(0.09)


class MurlingLine:
    def __init__(self, lineIndex, colorsArray):
        self.colors = colorsArray
        self.index = lineIndex

    def draw(self):

        if self.index < 0 or self.index > 15:
            return

        j = 0
        for i in range(16 * self.index, 16 * (self.index + 1)):
            setPixel(i, self.colors[j])
            j += 1

    def move(self, shift):
        self.index += shift


def murling(args):
    global pressed, modechanged

    screen_size = 16

    pixel_size = 1

    resolution = screen_size // pixel_size

    # matrix = [[[] for _ in range(resolution)] for _ in range(resolution)]

    def gray():
        light = rand(0, 255)
        return [light, light, light]

    # def make_perlin():
    #     for y in range(resolution):
    #         for x in range(resolution):
    #             # matrix[y][x] = edit_color(gray(), lambda light: abs(int(log2(abs(light + 1)))) * 1)
    #             matrix[y][x] = fix_color(gray())

    def make_perlin_line():
        return [fix_color([rand(0, 256), rand(0, 256), rand(0, 256)]) for _ in range(16)]

    # make_perlin()

    def randomize_color(color):
        a = 1.0 / float(int(timesecs()) % rand(3, 6) + 1)
        c = [color[0] // 2.4, color[1] // 1.6, color[2] * 1.25]

        hue = shift_hue(c, a)

        c = lerp_color(lerp_color(c, hue, 0.4), color, 0.1)

        return c

    lines = [MurlingLine(i, [[0,0,0] for _ in range(16)]) for i in range(16)]

    for i in range(16):
        lines[i].colors = make_perlin_line()
        lines[i].index = i

    while True:
        if pressed or modechanged:
            pressed = False
            modechanged = False
            return

        for i in range(screen_size):

            lines[i].move(-1)

            if not bounds(lines[i].index, 0, 15):
                lines[i].colors = make_perlin_line()
                lines[i].index = 15

            # for j in range(screen_size):
            #     c = matrix[i][j]
            #     color = randomize_color(c)
            #     # print(color)
            #     setPixel(i * 16 + j, Color(int(color[0]), int(color[1]), int(color[2])))
            # lines[i].colors = matrix[i]

        update()

        wait(uniform(0.0225, 0.045))


def calculate_waiting(schedule, current_time, dayofweek):

    print("CalculaTION")

    print(timesecs())

    enables = []
    hours = []
    mins = []

    sch = schedule.split(":")

    print(sch)

    for i in range(0, 21, 3):
        enables.append(int(sch[i]))

    for i in range(1, 21, 3):
        hours.append(int(sch[i]))

    for i in range(2, 21, 3):
        mins.append(int(sch[i]))

        #
        # if i % 3 == 0:
        #     mins.append(int(sch[i-1]))
        # elif i % 2 == 0:
        #     hours.append(int(sch[i-1]))
        # else:
        #     enables.append(int(sch[i-1]))

    print(enables, hours, mins)

    deltaday = 0

    targetdayofweek = repeat(dayofweek + 1, 0, 6)

    for i in range(7):
        if enables[targetdayofweek] == 0:
            deltaday += 1
            targetdayofweek = repeat(targetdayofweek + 1, 0, 6)
        else:
            break

    print("targetdayofweek = ", targetdayofweek)

    targetseconds = hours[targetdayofweek] * 3600 + mins[targetdayofweek] * 60 + deltaday * 86400

    print(targetseconds, current_time)

    print("COCOCOC")

    return targetseconds - current_time

sunriseon = True
waiting = False
dayofweekglobal = 0
def sunrise(schedule, current_time, dayofweek):
    global sunriseon, waiting, pressed, modechanged, dayofweekglobal

    dayofweekglobal = dayofweek

    print("Sunrise Enabled!", schedule, time, dayofweek)

    while sunriseon:

        if not waiting:
            waiting = True
            fill(Color(0, 0, 0))

            target_time = calculate_waiting(schedule, current_time, dayofweekglobal)

            step = (target_time - current_time) / 10000.0

            # wait(target_time - current_time)

            print(target_time, current_time, step)
            for i in range(10000):
                wait(step)
                print(f"Waited! {10000-i} times left by {step} seconds")
                if not sunriseon:
                    sunriseon = True
                    print("Sunrise aborted")
                    fill(Color(0, 100, 0))
                    return
                if pressed or modechanged:
                    pressed = False
                    modechanged = False
                    return
        else:
            waiting = False

        # if not sunriseon:
        #     sunriseon = True
        #     return

        print("SUNRISEEE start")


        step = 300.0 / 255.0

        for i in range(255):
            if not sunriseon:
                sunriseon = True
                print("Sunrise aborted")
                fill(Color(0, 100, 0))
                return
            color = Color(i, i, 0)
            print(color)
            fill(color)
            # wait(0.1)
            wait(step)

        print("SUNRISEEE end")

        for i in range(1200):
            wait(1)
            if not sunriseon:
                sunriseon = True
                print("Sunrise endededed")
                fill(Color(0, 0, 0))

                dayofweekglobal = repeat(dayofweekglobal, 0, 6)

                return