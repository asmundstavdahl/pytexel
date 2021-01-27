#!/bin/env python3

import pygame
from pygame.locals import *
from pygame import draw
import numpy as np
import time
from PIL import Image
from texelator import Texelator

texelator: Texelator = Texelator()

pygame.init()
CFg: pygame.Color = pygame.Color("black")
CBg: pygame.Color = pygame.Color("white")
displaySize = (500, 500)
ballRadius = 50
texplaySize = (40, 20)
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
pos = (displaySize[0] // 2, displaySize[1] // 2)
v = (2.0, 1.0)
gravity = 9.8  # m/s/s

tPrev = time.time() - frameTime
while True:
    # Frame preparation
    (dt, tPrev) = waitForNextFrame(tPrev)
    display.fill(CBg)

    # Behaviour
    v = (v[0], v[1] + gravity * dt)
    pos = (
        pos[0] + v[0],
        pos[1] + v[1],
    )
    pos = (
        max(0 + ballRadius, min(displaySize[0] - ballRadius, pos[0])),
        max(0 + ballRadius, min(displaySize[1] - ballRadius, pos[1])),
    )
    if pos[0] + v[0]*dt + ballRadius > displaySize[0] or pos[0] + v[0]*dt - ballRadius < 0:
        v = (
            -v[0],
            v[1],
        )
    if pos[1] + v[1]*dt + ballRadius > displaySize[1] or pos[1] + v[1]*dt - ballRadius < 0:
        v = (
            v[0],
            -v[1],
        )



    # Drawing
    draw.circle(display, CFg, (
        int(pos[0]), int(pos[1])),
        ballRadius)

    # Texelate pygame surface
    displayBuffer: pygame.BufferProxy = display.get_buffer()
    image = Image.frombuffer(
        "RGBX", displaySize, displayBuffer, "raw", "RGBX", 0, 1)
    output = texelator.render(image, texplaySize[0], texplaySize[1])
    print("\x1b[H")
    print(output)

print()
