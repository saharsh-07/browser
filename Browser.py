import tkinter
from URL import *

# page coordination helper function
def layout(text):
  display_list = [] # display_list is standard name for list of things to display
  cursor_x, cursor_y = HSTEP, VSTEP 
  for c in text:
    display_list.append((cursor_x, cursor_y, c)) # horizontal, vertical delta, characters in text
    cursor_x += HSTEP # keep displaying with diff of horiz delta
    if cursor_x >= WIDTH - HSTEP: # if end of line (line-wrap)
      cursor_y += VSTEP # next column (verical)
      cursor_x = HSTEP  # start of row (horizontal)

  return display_list


class Browser:
  def __init__(self):
    global HEIGHT, WIDTH, HSTEP, VSTEP, SCROLL_STEP
    HEIGHT, WIDTH = 600, 800  # height and width of window
    HSTEP, VSTEP = 13, 18 # vertical and horizontal placing delta
    self.scroll = 0 # how much scrolled
    SCROLL_STEP = 100  # scroll this much scrolled using button
    self.window = tkinter.Tk()
    self.canvas = tkinter.Canvas(self.window, height=HEIGHT, width=WIDTH)
    self.canvas.pack()  # keeps canvas under window
    self.window.bind("<Down>", self.scroll_down)  # event of down keypress (for scrolling)
  
  # helper function for scrolling
  def scroll_down(self, e):
    self.scroll += SCROLL_STEP
    self.draw()

  # function for displaying
  def draw(self):
    self.canvas.delete("all") # repainting every time
    for x, y, c in self.display_list:
      self.canvas.create_text(x, y - self.scroll, text=c)

  def load(self, url):
    body = URL.request(url)
    text = lex(body)
    self.display_list = layout(text)
    self.draw()
        

if __name__ == "__main__":
  import sys
  Browser().load(URL(sys.argv[1]))
  tkinter.mainloop()