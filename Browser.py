import tkinter
import tkinter.font
from URL import *
from HTMLParser import *
from Document_Layout import *
from GLOBALS import *
        
class Browser:
  def __init__(self):
    self.window = tkinter.Tk()
    self.canvas = tkinter.Canvas(
        self.window,
        width=WIDTH,
        height=HEIGHT
    )
    self.canvas.pack()

    self.scroll = 0
    self.window.bind("<Down>", self.scroll_down)

  def load(self, url):
    body = url.request()
    self.nodes = HTMLParser(body).parse()

    self.document = Document_Layout(self.nodes)
    self.document.layout()  # making layout document tree
    self.display_list = []
    paint_tree(self.document, self.display_list)
    self.draw()


  # function for displaying
  def draw(self):
        self.canvas.delete("all")
        for cmd in self.display_list:
            if cmd.top > self.scroll + HEIGHT: continue
            if cmd.bottom < self.scroll: continue
            cmd.execute(self.scroll, self.canvas)

  # helper function for scrolling
  def scroll_down(self, e):
    max_y = max(self.document.height + 2*VSTEP - HEIGHT, 0)
    self.scroll = min(self.scroll + SCROLL_STEP, max_y)
    self.draw()

        

if __name__ == "__main__":
  import sys
  Browser().load(URL(sys.argv[1]))
  tkinter.mainloop()