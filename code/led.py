import time
import machine
import neopixel

class Led():
  np = None
  nrows = 3
  cur = None
  start = None
  buf = []
  delay = 0
  cur_t = 0

  def __init__(self):
    self.np = neopixel.NeoPixel(machine.Pin(0), 30, 4)

  def clear(self):
    self.buf = []
    self.cur_t = 0
    self.np.fill((0, 0, 0, 0))
    self.np.write()

  def set_col_pixel(self, colnum, rgbw):
    n = int(self.np.n / self.nrows)
    for r in range(self.nrows):
      # Order is flipped on every other row
      if r%2: self.np[r*n+(n-colnum)] = rgbw
      else: self.np[r*n+colnum] = rgbw

  def set_row_pixel(self, rownum, rgbw):
    n = int(self.np.n / self.nrows)
    for r in range(self.nrows):
      s = r*n
      for i in range(n):
        self.np[s+i] = row_rgbw[i] if r%2 else row_rgbw[n-i-1]

  def heartbeat(self, rgbw=(255,0,0,0)):
    for i in [x for x in range(255)]+[x for x in range(255,-1,-1)]:
      self.np.fill([int(i/255. * v) for v in rgbw])
      self.np.write()
      time.sleep_ms(1)

  def scanner_init(self, delay=2, rgbw=(255,0,0,0), back=(0,50,255,50)):
    self.start = time.time()
    self.delay = delay
    self.cur_t = 0
    self.type = 's'
    #self.buf = (i for j in (range(10), range(9,-1,-1)) for i in j)
    self.buf = [i for j in (range(9), range(9,0,-1)) for i in j]
    self.colors = {'back':back, 'rgbw':rgbw}

  def update(self):
    if len(self.buf)>0:
      now = time.time()
      # check timing here
      if self.type=='s':
        self.np.fill(self.colors['back'])
        self.set_col_pixel(self.buf[self.cur_t],self.colors['rgbw'])
        self.cur_t += 1
        if self.cur_t>=len(self.buf):
          self.cur_t = 0
      self.np.write()

  def bounce(self):
   for i in range(4 * n):
     self.np.fill((200, 200, 200, 200))
     if (i // n) % 2 == 0:
         self.np[i % n] = (0, 0, 0, 0)
     else:
         self.np[n - 1 - (i % n)] = (0, 0, 0, 0)
     self.np.write()

  def fade(self):
    for c in range(3):
      rgbw = [0,0,0,0]
      rgbw[c] = 255
      for i in range(4 * n):
        self.np.fill(rgbw)
        if (i // n) % 2 == 0:
          self.np[i % n] = (0, 0, 0, 0)
        else:
          self.np[n - 1 - (i % n)] = (0, 0, 0, 0)
        self.np.write()


