#!/usr/bin/python
"""
Python/PIL version of Kim Asendorf's ASDFPixelSort
https://github.com/kimasendorf/ASDFPixelSort

Usage: ASDFPixelSort.py imgfilename [mode]

Mode:
0 -> black
1 -> bright (default)
2 -> white
"""
import os
import sys

from PIL import Image

try: import timing # optional
except: pass

blackValue = (11, 220, 0) # corresponds to Processing's -16000000
brightnessValue = 60
whiteValue = (57, 162, 192) # corresponds to Processing's -13000000

row = 0
column = 0

# A stripped down version of colorsys.rgb_to_hsv()
def brightness(x, y):
    """
    Return the maximum of a pixel's red, green and blue values.
    This is the same as converting from RGB to HSV (aka HSB) then returning the V (aka B) component.
    """
    return max(pixels[x, y])
    
def sortRow():
    x = 0
    y = row
    xend = 0
  
    while(xend < width-1):
        if mode == 0:
            x = getFirstNotBlackX(x, y)
            xend = getNextBlackX(x, y)
        elif mode == 1:
            x = getFirstBrightX(x, y)
            xend = getNextDarkX(x, y)
        elif mode == 2:
            x = getFirstNotWhiteX(x, y)
            xend = getNextWhiteX(x, y)
        else:
            break
        
        if x < 0: break
    
        sortLength = xend-x
        
        unsorted_colors = []
        sorted_colors = []
        
        for i in range(0, sortLength):
          unsorted_colors.append(pixels[x+i, y])
        
        sorted_colors = sorted(unsorted_colors)
        
        for i in range(0, sortLength):
          pixels[x+i, y] = sorted_colors[i]
    
        x = xend+1

def sortColumn():
    x = column
    y = 0
    yend = 0
  
    while(yend < height-1):
        if mode == 0:
            y = getFirstNotBlackY(x, y)
            yend = getNextBlackY(x, y)
        elif mode == 1:
            y = getFirstBrightY(x, y)
            yend = getNextDarkY(x, y)
        elif mode == 2:
            y = getFirstNotWhiteY(x, y)
            yend = getNextWhiteY(x, y)
        else:
            break
    
        if y < 0: break
    
        sortLength = yend-y
        
        unsorted_colors = []
        sorted_colors = []
        
        for i in range(0, sortLength):
            unsorted_colors.append(pixels[x, y+i])
        
        sorted_colors = sorted(unsorted_colors)
        
        for i in range(0, sortLength):
          pixels[x, y+i] = sorted_colors[i]
        
        y = yend+1

# BLACK
def getFirstNotBlackX(_x, _y):
    x = _x
    y = _y
    while(pixels[x, y] < blackValue):
        x += 1
        if(x >= width): return -1
    return x

def getNextBlackX(_x, _y):
    x = _x+1
    y = _y
    if(x >= width): return width-1
    while(pixels[x, y] > blackValue):
        x += 1
        if(x >= width): return width-1
    return x-1

# BRIGHTNESS
def getFirstBrightX(_x, _y):
    x = _x
    y = _y
    while(brightness(x, y) < brightnessValue):
        x += 1
        if(x >= width): return -1
    return x

def getNextDarkX(_x, _y):
    x = _x+1
    y = _y
    if(x >= width): return width-1
    while(brightness(x, y) > brightnessValue):
        x += 1
        if(x >= width): return width-1
    return x-1

# WHITE
def getFirstNotWhiteX(_x, _y):
    x = _x
    y = _y
    while(pixels[x, y] > whiteValue):
        x += 1
        if(x >= width): return -1
    return x

def getNextWhiteX(_x, _y):
    x = _x+1
    y = _y
    if(x >= width): return width-1
    while(pixels[x, y] < whiteValue):
        x += 1
        if(x >= width): return width-1
    return x-1

# BLACK
def getFirstNotBlackY(_x, _y):
    x = _x
    y = _y
    if(y < height):
        while(pixels[x, y] < blackValue):
          y += 1
          if(y >= height): return -1
    return y

def getNextBlackY(_x, _y):
    x = _x
    y = _y+1
    if(y < height):
        while(pixels[x, y] > blackValue):
            y += 1
            if(y >= height): return height-1
    return y-1

# BRIGHTNESS
def getFirstBrightY(_x, _y):
    x = _x
    y = _y
    if(y < height):
        while(brightness(x, y) < brightnessValue):
            y += 1
            if(y >= height): return -1
    return y

def getNextDarkY(_x, _y):
    x = _x
    y = _y+1
    if(y < height):
        while(brightness(x, y) > brightnessValue):
            y += 1
            if(y >= height): return height-1
    return y-1

# WHITE
def getFirstNotWhiteY(_x, _y):
    x = _x
    y = _y
    if(y < height):
        while(pixels[x, y] > whiteValue):
            y += 1
            if(y >= height): return -1
    return y

def getNextWhiteY(_x, _y):
    x = _x
    y = _y+1
    if(y < height):
        while(pixels[x, y] < whiteValue):
            y += 1
            if(y >= height): return height-1
    return y-1
    
if __name__ == '__main__':
    filename, file_type = os.path.splitext(sys.argv[1])

    if len(sys.argv) > 2:
        mode = int(sys.argv[2])
    else:
        mode = 1

    # Setup
    print "Load image"
    img = Image.open(filename + file_type)
    # img = img.convert('RGB')
    width, height = img.size
    pixels = img.load()
    
    # Draw
    print "Sort columns"
    while(column < width-1):
        sortColumn()
        column += 1
  
    print "Sort rows"
    while(row < height-1):
        sortRow()
        row += 1
  
    outfile = filename + "_" + str(mode) + ".png"
    print "Saving to", outfile
    img.save(outfile, quality=100)
    print("DONE")
