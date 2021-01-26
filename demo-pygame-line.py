#!/bin/env python3

import pygame
from pygame.locals import *
import numpy as np
from PIL import Image
from texelator import Texelator

texelator: Texelator = Texelator()

pygame.init()
CFg: pygame.Color = pygame.Color("black")
CBg: pygame.Color = pygame.Color("white")
displaySize = (500, 500)

print("\n"*90)

display = pygame.surface.Surface(displaySize)

for i in range(450):
    display.fill(CBg)

    pygame.draw.line(display, CFg, (50, 50 + i),
                     ((350 + 10*i) % displaySize[1], 250), 10)
    displayBuffer: pygame.BufferProxy = display.get_buffer()

    image = Image.frombuffer(
        "RGBX", displaySize, displayBuffer, "raw", "RGBX", 0, 1)

    output = texelator.render(image, 60, 30)
    print(output)
    print("\x1b[H")
