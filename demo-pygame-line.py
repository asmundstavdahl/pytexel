#!/bin/env python3

import pygame
from pygame.locals import *
import numpy as np
import time
from PIL import Image
from pytexel.texelator import Texelator

texelator: Texelator = Texelator()

pygame.init()
CFg: pygame.Color = pygame.Color("black")
CBg: pygame.Color = pygame.Color("white")
displaySize = (500, 500)
texplaySize = (20, 10)
frameTime = (1/60)


def waitForNextFrame(tPrev) -> (float, float):
    tNow = time.time()
    dt = tNow - tPrev
    if dt < frameTime:
        time.sleep(frameTime - dt)
        tNow = time.time()
        dt = tNow - tPrev
    tPrev = tNow
    print(f"FPS={(1/dt) - (1/dt) % 0.1}")
    return (dt, tPrev)


print("\x1b[2J")
print("\x1b[H")
print("\n" * texplaySize[1])

display = pygame.surface.Surface(displaySize)

tPrev = time.time() - frameTime
for i in range(450):
    (dt, tPrev) = waitForNextFrame(tPrev)

    display.fill(CBg)

    pygame.draw.line(display, CFg, (50, 50 + i),
                     ((350 + 10*i) % displaySize[1], 250), 10)
    displayBuffer: pygame.BufferProxy = display.get_buffer()

    image = Image.frombuffer(
        "RGBX", displaySize, displayBuffer, "raw", "RGBX", 0, 1)

    output = texelator.render(image, texplaySize[0], texplaySize[1])
    print("\x1b[H")
    print(output)

print()
