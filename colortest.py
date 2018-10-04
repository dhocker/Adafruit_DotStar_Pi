#!/usr/bin/python

#
# Designed to try out colors on dotstar strip and generally learn more
# about the Adafruit DotStar library.
#

import time
import random
from collections import deque
from dotstar import Adafruit_DotStar

#
# Gamma correction table
# See https://learn.adafruit.com/led-tricks-gamma-correction/the-issue
#
gamma8 = [
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255]

numpixels = 30 # Number of LEDs in strip under test
delay_time = 0.020 # 20 ms delay between writing pixels
brightness = 16 # 1/8 duty cycle for lower power

# For SPI
datapin = 10    # GPIO/BCM 10 SPI_MOSI
clockpin = 11   # GPIO/BCM 11 SPI_SCLK

def Color(r, g, b, gamma=False):
    # Based on empiracle observation that the order is bgr = bbggrr
    if gamma:
        return ((gamma8[b] << 16) | (gamma8[g] << 8) | gamma8[r]) & 0xFFFFFF
    return ((b << 16) | (g << 8) | r) & 0xFFFFFF

def rgb_color(r, g, b):
    # Based on empiracle observation that the order is bgr = bbggrr
    return ((b << 16) | (g << 8) | r) & 0xFFFFFF

def gamma_color(r, g, b):
    # Gamma adjusted color values
    # Based on empiracle observation that the order is bgr = bbggrr
    return ((gamma8[b] << 16) | (gamma8[g] << 8) | gamma8[r]) & 0xFFFFFF

def rgb(c):
    """
    Returns [r, g, b] assuming c is in order bgr as required by DotStar
    """
    return [c & 0xFF, c >> 8 & 0xFF, c >> 16 & 0xFF]

def wheel(pos, gamma=False):
    """
    Generate rainbow colors across 0-255 positions.
    This is mostly an algorithm that generates a continuous color
    change over the range 0-255.
    """
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0, gamma=gamma)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3, gamma=gamma)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3, gamma=gamma)

def wheel_fill(strip, iterations=1):
    print("Wheel with gamma correction")
    for i in range(iterations):
        for pos in range(256):
            c = wheel(pos, gamma=True)
            print(pos, rgb(c))
            for pxl in range(numpixels):
                strip.setPixelColor(pxl, c)
            strip.show()
            time.sleep(0.5)

def solid_fill(strip, c, iterations=1):
    for i in range(iterations):
        for pxl in range(numpixels):
            strip.setPixelColor(pxl, c)
        strip.show()
        time.sleep(1.0)

def scroll_pixels(strip, test_color, iterations):
    # Runs 10 LEDs at a time along strip
    
    head  = 0               # Index of first 'on' pixel
    # tail  = -10             # Index of last 'off' pixel
    tail = -5

    for i in range(iterations): # Loop for number of iterations
    
        strip.setPixelColor(head, test_color) # Turn on 'head' pixel
        if tail >= 0:
            strip.setPixelColor(tail, 0)     # Turn off 'tail'
        strip.show()                     # Refresh strip
        time.sleep(delay_time)           # Pause for delay time
        
        head += 1                        # Advance head position
        if(head >= numpixels):           # Off end of strip?
            head    = 0              # Reset to start

        tail += 1                        # Advance tail position
        if(tail >= numpixels): 
            tail = 0  # Off end? Reset
    
    print("Turning off all lights...")
    # Not well documented, but this is how you turn
    # off everything
    strip.clear()
    strip.show()

def get_random_int(max_value=100):
    return int(random.random() * max_value)

def get_random_color(brightness=2):
    r = int(get_random_int(max_value=255) / brightness)
    g = int(get_random_int(max_value=255) / brightness)
    b = int(get_random_int(max_value=255) / brightness)
    return Color(r, g, b)

def random_pixels(strip):    
    pixels = deque()
    active_size = int(strip.numPixels() / 2)
    color = Color(255, 0, 0)

    print("{0} random pixels for 10 sec...".format(strip.numPixels()))
    for i in range(int(10.0 / delay_time)):
        if len(pixels) >= active_size:
            p = pixels.pop()
            strip.setPixelColor(p, 0)
        p = get_random_int(max_value=strip.numPixels())
        pixels.appendleft(p)
        strip.setPixelColor(p, get_random_color())
        strip.show()
        time.sleep(delay_time)
    strip.clear()

def main():
    
    # Alternate ways of declaring strip:
    # Only use hardware SPI
    # print "Data pin GPIO/BCM {0}".format(datapin)
    # print "Clock pin GPIO/BCM {0}".format(clockpin)
    print("Opening LED strip with {0} pixels".format(numpixels))
    # NOTE: This is not the same as omitting data/clock pin args!!!
    # strip = Adafruit_DotStar(numpixels, datapin, clockpin, order='gbr') # Use SPI (pins 10=MOSI, 11=SCLK)
    # strip = Adafruit_DotStar(numpixels, datapin, clockpin, order='grb') # Use SPI (pins 10=MOSI, 11=SCLK)
    # strip = Adafruit_DotStar(numpixels) # Use SPI (pins 10=MOSI, 11=SCLK)
    # strip = Adafruit_DotStar(numpixels, order='gbr') # Use SPI (pins 10=MOSI, 11=SCLK)
    # NOTE: The default color order is BRG (not RGB)
    strip = Adafruit_DotStar(numpixels, order='rgb'.encode('utf-8')) # Use SPI (pins 10=MOSI, 11=SCLK)
    strip.begin()           # Initialize pins for output

    strip.setBrightness(brightness) # Limit brightness
    #strip.setBrightness(127) # Unlimited brightness
    
    print("Hit Ctrl-C to end test")
    
    try:
        while True:
            # scroll_pixels(strip, Color(255, 83, 13), numpixels * 20)
            # This one pretty much produces the expected results (gamma applied)
            #scroll_pixels(strip, Color(255, 83, 13, gamma=True), numpixels * 20)
            #scroll_pixels(strip, rgb_color(255, 0, 0), numpixels * 20)
            #scroll_pixels(strip, rgb_color(0, 255, 0), numpixels * 20)
            #scroll_pixels(strip, rgb_color(0, 0, 255), numpixels * 20)
            #solid_fill(strip, Color(255, 0, 0, gamma=True), iterations=2)
            #solid_fill(strip, Color(0, 255, 0, gamma=True), iterations=2)
            #solid_fill(strip, Color(0, 0, 255, gamma=True), iterations=2)
            wheel_fill(strip, iterations=1)
            print("Pass complete")
    except (KeyboardInterrupt, Exception) as ex:
        print(ex)
        print("")
        print("Turning off all lights...")
        # Not well documented, but this is how you turn
        # off everything
        strip.clear()
        strip.show()

        strip.close()
        print("Strip closed")
    
    
if __name__ == "__main__":
    main()
