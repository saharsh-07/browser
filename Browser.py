import tkinter
import tkinter.font
from URL import *
from HTMLParser import *
from Layout import *
from GLOBALS import *

class Browser:
  def __init__(self):
    self.window = tkinter.Tk()
    self.canvas = tkinter.Canvas(self.window, height=HEIGHT, width=WIDTH)
    self.canvas.pack()  # keeps canvas under window

    self.scroll = 0 # how much scrolled
    self.window.bind("<Down>", self.scroll_down)  # event of down keypress (for scrolling)
    self.display_list = []
  
  def load(self, url):
    body = url.request()
    self.nodes = HTMLParser(body).parse()
    self.display_list = Layout(self.nodes).display_list
    self.draw()

  # function for displaying
  def draw(self):
    self.canvas.delete("all") # repainting every time
    for x, y, word, font in self.display_list:
      # optimizations for achieving 16ms (ideal animation frame budget) (1/60 second time for drawing)
      if y  > self.scroll + HEIGHT: continue  # skip render of text below (window)view
      if y + VSTEP < self.scroll : continue   # skip render of text above view
      
      self.canvas.create_text(x, y - self.scroll, text=word, font=font, anchor="nw")

  # helper function for scrolling
  def scroll_down(self, e):
    self.scroll += SCROLL_STEP
    self.draw()

        

if __name__ == "__main__":
  import sys
  Browser().load(URL(sys.argv[1]))
  tkinter.mainloop()