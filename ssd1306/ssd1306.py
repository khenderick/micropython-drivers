import pyb

# Constants
DISPLAYOFF          = 0xAE
SETCONTRAST         = 0x81
DISPLAYALLON_RESUME = 0xA4
DISPLAYALLON        = 0xA5
NORMALDISPLAY       = 0xA6
INVERTDISPLAY       = 0xA7
DISPLAYON           = 0xAF
SETDISPLAYOFFSET    = 0xD3
SETCOMPINS          = 0xDA
SETVCOMDETECT       = 0xDB
SETDISPLAYCLOCKDIV  = 0xD5
SETPRECHARGE        = 0xD9
SETMULTIPLEX        = 0xA8
SETLOWCOLUMN        = 0x00
SETHIGHCOLUMN       = 0x10
SETSTARTLINE        = 0x40
MEMORYMODE          = 0x20
COLUMNADDR          = 0x21
PAGEADDR            = 0x22
COMSCANINC          = 0xC0
COMSCANDEC          = 0xC8
SEGREMAP            = 0xA0
CHARGEPUMP          = 0x8D
EXTERNALVCC         = 0x10
SWITCHCAPVCC        = 0x20
SETPAGEADDR         = 0xB0
SETCOLADDR_LOW      = 0x00
SETCOLADDR_HIGH     = 0x10
ACTIVATE_SCROLL                      = 0x2F
DEACTIVATE_SCROLL                    = 0x2E
SET_VERTICAL_SCROLL_AREA             = 0xA3
RIGHT_HORIZONTAL_SCROLL              = 0x26
LEFT_HORIZONTAL_SCROLL               = 0x27
VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = 0x29
VERTICAL_AND_LEFT_HORIZONTAL_SCROLL  = 0x2A

class SSD1306(object):

  def __init__(self, pinout, height=32, external_vcc=True):
    self.external_vcc = external_vcc
    self.height       = 32 if height == 32 else 64
    self.pages        = int(self.height / 8)
    self.columns      = 128

    rate = 16 * 1024 * 1024

    self.spi = pyb.SPI(2, pyb.SPI.MASTER, baudrate=rate, polarity=1, phase=0)  # SCK: Y6: MOSI: Y8
    self.dc  = pyb.Pin(pinout['dc'],  pyb.Pin.OUT_PP, pyb.Pin.PULL_DOWN)
    self.res = pyb.Pin(pinout['res'], pyb.Pin.OUT_PP, pyb.Pin.PULL_DOWN)

  def clear(self):
    self.buffer = bytearray(self.pages * self.columns)  

  def write_command(self, command_byte):
    self.dc.low()
    self.spi.send(command_byte)

  def write_data(self, data_byte):
    self.dc.high()
    self.spi.send(data_byte)

  def invert_display(self, invert):
    self.write_command(INVERTDISPLAY if invert else NORMALDISPLAY)

  def display(self):
    self.write_command(COLUMNADDR)
    self.write_command(0)
    self.write_command(self.columns - 1)
    self.write_command(PAGEADDR)
    self.write_command(0)
    self.write_command(self.pages - 1)

    self.dc.high()
    self.spi.send(self.buffer)

  def set_pixel(self, x, y, state):
    index = x + (int(y / 8) * self.columns)
    if state:
      self.buffer[index] |= (1 << (y & 7))
    else:
      self.buffer[index] &= ~(1 << (y & 7))

  def init_display(self):
    chargepump = 0x10 if self.external_vcc else 0x14
    precharge  = 0x22 if self.external_vcc else 0xf1
    multiplex  = 0x1f if self.height == 32 else 0x3f
    compins    = 0x02 if self.height == 32 else 0x12
    contrast   = 0xff # 0x8f if self.height == 32 else (0x9f if self.external_vcc else 0x9f)
    data = [DISPLAYOFF,
            SETDISPLAYCLOCKDIV, 0x80,
            SETMULTIPLEX, multiplex,
            SETDISPLAYOFFSET, 0x00,
            SETSTARTLINE | 0x00,            
            CHARGEPUMP, chargepump,
            MEMORYMODE, 0x00,
            SEGREMAP | 0x10,
            COMSCANDEC,
            SETCOMPINS, compins,
            SETCONTRAST, contrast,
            SETPRECHARGE, precharge,
            SETVCOMDETECT, 0x40,
            DISPLAYALLON_RESUME,
            NORMALDISPLAY,
            DISPLAYON]
    for item in data:                     
      self.write_command(item)
    self.clear()
    self.display()

  def poweron(self):
    self.res.high()
    pyb.delay(1)
    self.res.low()
    pyb.delay(10)
    self.res.high()
    pyb.delay(10)

  def poweroff(self):
    self.write_command(0xae)  # Set display off
