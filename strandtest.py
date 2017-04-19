#!/usr/bin/python

# Simple strand test for Adafruit Dot Star RGB LED strip.
# This is a basic diagnostic tool, NOT a graphics demo...helps confirm
# correct wiring and tests each pixel's ability to display red, green
# and blue and to forward data down the line.  By limiting the number
# and color of LEDs, it's reasonably safe to power a couple meters off
# USB.  DON'T try that with other code!

import time
import random
from collections import deque
from dotstar import Adafruit_DotStar
from effects import *

"""
These are the methods that are available on the Adafruit_DotStar
strip object. This doc was taken from the dotsar.c source code.
  { "begin"        , (PyCFunction)begin        , METH_NOARGS , NULL },
  { "clear"        , (PyCFunction)clear        , METH_NOARGS , NULL },
  { "setBrightness", (PyCFunction)setBrightness, METH_VARARGS, NULL },
  { "setPixelColor", (PyCFunction)setPixelColor, METH_VARARGS, NULL },
  { "show"         , (PyCFunction)show         , METH_VARARGS, NULL },
  { "Color"        , (PyCFunction)Color        , METH_VARARGS, NULL },
  { "getPixelColor", (PyCFunction)getPixelColor, METH_VARARGS, NULL },
  { "numPixels"    , (PyCFunction)numPixels    , METH_NOARGS , NULL },
  { "getBrightness", (PyCFunction)getBrightness, METH_NOARGS , NULL },
  { "getPixels"    , (PyCFunction)getPixels    , METH_NOARGS , NULL },
  { "close"        , (PyCFunction)_close       , METH_NOARGS , NULL },
"""

numpixels = 30 # Number of LEDs in strip under test
delay_time = 0.020 # 20 ms delay between writing pixels
brightness = 16 # 1/8 duty cycle for lower power

# Here's how to control the strip from any two GPIO pins:
# datapin   = 23
# clockpin  = 24
# strip     = Adafruit_DotStar(numpixels, datapin, clockpin)

# For SPI
datapin = 10    # GPIO/BCM 10 SPI_MOSI
clockpin = 11   # GPIO/BCM 11 SPI_SCLK

def scroll_pixels(strip, iterations):
    # Runs 10 LEDs at a time along strip, cycling through red, green and blue.
    # This requires about 200 mA for all the 'on' pixels + 1 mA per 'off' pixel.
    
    head  = 0               # Index of first 'on' pixel
    # tail  = -10             # Index of last 'off' pixel
    tail = -5
    starting_color = 0xFF0000
    color_shift = 8
    # color = 0xFF0000        # 'On' color (starts red)
    color = starting_color
    
    for i in range(iterations): # Loop for number of iterations
    
        try:
            strip.setPixelColor(head, color) # Turn on 'head' pixel
            if tail >= 0:
                strip.setPixelColor(tail, 0)     # Turn off 'tail'
            strip.show()                     # Refresh strip
            # time.sleep(1.0 / 50)             # Pause 20 milliseconds (~50 fps)
            time.sleep(delay_time)           # Pause for delay time
            
            head += 1                        # Advance head position
            if(head >= numpixels):           # Off end of strip?
                head    = 0              # Reset to start
                # color >>= 8              # Red->green->blue->black
                color >>= color_shift                # Red->green->blue->black
                if(color == 0): 
                    # color = 0xFF0000 # If black, reset to red
                    color = starting_color # If black, reset
    
            tail += 1                        # Advance tail position
            if(tail >= numpixels): 
                tail = 0  # Off end? Reset
    
        except KeyboardInterrupt:
            break

    print "Turning off all lights..."
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

    print "{0} random pixels for 10 sec...".format(strip.numPixels())
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
    print "Data pin GPIO/BCM {0}".format(datapin)
    print "Clock pin GPIO/BCM {0}".format(clockpin)
    print "Opening LED strip with {0} pixels".format(numpixels)
    # The default here is SPI at 800 KHz
    # strip   = Adafruit_DotStar(numpixels)           # Use SPI (pins 10=MOSI, 11=SCLK by default)
    # This strip uses the specified pins at 800 KHz
    #strip   = Adafruit_DotStar(numpixels, datapin, clockpin, order='gbr') # Use SPI (pins 10=MOSI, 11=SCLK)
    strip   = Adafruit_DotStar(numpixels, order='gbr') # Use SPI (pins 10=MOSI, 11=SCLK)
    # strip   = Adafruit_DotStar(numpixels, 32000000) # SPI @ ~32 MHz
    # strip   = Adafruit_DotStar()                    # SPI, No pixel buffer
    # strip   = Adafruit_DotStar(32000000)            # 32 MHz SPI, no pixel buf
    # See image-pov.py for explanation of no-pixel-buffer use.
    # Append "order='gbr'" to declaration for proper colors w/older DotStar strips)
    
    strip.begin()           # Initialize pins for output
    # strip.setBrightness(64) # Limit brightness to ~1/4 duty cycle
    strip.setBrightness(brightness) # Limit brightness
    # Runs 10 LEDs at a time along strip, cycling through red, green and blue.
    # This requires about 200 mA for all the 'on' pixels + 1 mA per 'off' pixel.
    
    print "Hit Ctrl-C to end test"
    
    try:
        while True:
            random_pixels(strip)
            run_all_effects(strip)
            scroll_pixels(strip, numpixels * 20)
    except (KeyboardInterrupt, Exception) as ex:
        print ex
        print ""
        print "Turning off all lights..."
        # Not well documented, but this is how you turn
        # off everything
        strip.clear()
        strip.show()

        strip.close()
        print "Strip closed"
    
    
if __name__ == "__main__":
    main()
