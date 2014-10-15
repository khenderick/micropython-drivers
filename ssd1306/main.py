# The MIT License (MIT)
#
# Copyright (c) 2014 Kenneth Henderick
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import pyb
from ssd1306 import SSD1306

# SPI
display = SSD1306(pinout={'dc': 'Y3',
                          'res': 'Y4'},
                  height=64,
                  external_vcc=False)

# I2C connected to Y9, Y10 (I2C bus 2)
# display = SSD1306(pinout={'sda': 'Y10',
#                           'scl': 'Y9'},
#                   height=64,
#                   external_vcc=False)

led_red = pyb.LED(1)
led_red.off()

try:
  display.poweron()
  display.init_display()

  x = 0
  y = 0
  direction_x = True
  direction_y = True

  while True:
    # Clear the previous lines
    prev_x = x
    prev_y = y

    # Move bars
    x += (1 if direction_x else -1)
    y += (1 if direction_y else -1)

    # Bounce back, if required
    if x == 128:
       direction_x = False
       x = 126
    elif x == -1:
       direction_x = True
       x = 1
    if y == 64:
       direction_y = False
       y = 63
    elif y == -1:
       direction_y = True
       y = 1

    # Draw new lines
    for i in range(64):
      display.set_pixel(prev_x, i, False)
      display.set_pixel(x, i, True)
    for i in range(128):
      display.set_pixel(i, prev_y, False)
      display.set_pixel(i, y, True)
 
    # Make sure the corners are active
    display.set_pixel(0,   0,  True)
    display.set_pixel(127, 0,  True)
    display.set_pixel(0,   63, True)
    display.set_pixel(127, 63, True)
    
    # Write display buffer
    display.display()

except Exception as ex:
  led_red.on()
  print('Unexpected error: {0}'.format(ex))
  display.poweroff()
