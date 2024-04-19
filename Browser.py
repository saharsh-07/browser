import tkinter
from URL import *

class Browser:
  def __init__(self):
    global HEIGHT
    global WIDTH
    HEIGHT, WIDTH = 600, 800
    self.window = tkinter.Tk()
    self.canvas = tkinter.Canvas(self.window, height=HEIGHT, width=WIDTH)
    self.canvas.pack()
  
  def load(self, url):
    HSTEP, VSTEP = 13, 18 # vertical and horizontal placing delta
    cursor_x, cursor_y = HSTEP, VSTEP
    body = URL.request(url)
    text = lex(body)
    for c in text:
      self.canvas.create_text(cursor_x, cursor_y, text=c)
      cursor_x += HSTEP
      if cursor_x >= WIDTH - HSTEP:
        cursor_y += VSTEP
        cursor_x = HSTEP
        

if __name__ == "__main__":
  import sys
  Browser().load(URL(sys.argv[1]))
  tkinter.mainloop()