import tkinter
import tkinter.font
from URL import *


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

    global BI_TIMES
    BI_TIMES = tkinter.font.Font(
            family="Times",
            size=16,
            weight="bold",
            slant="italic",
        )
  
  # page coordination helper function
  def layout(tokens):
    display_list = [] # display_list is standard name for list of things to display
    cursor_x, cursor_y = HSTEP, VSTEP
    weight = "normal"
    style = "roman"
    font = tkinter.font.Font() 
    for tok in tokens:
      if isinstance(tok, Text):
        for word in tok.text.split():
          font = tkinter.font.Font(
              size=16,
              weight=weight,
              slant=style,
          )
          w = font.measure(word)
          display_list.append((cursor_x, cursor_y, word, font)) # horizontal, vertical delta, characters in text
          cursor_x += w + font.measure(" ") # keep displaying with diff of horiz delta
          if cursor_x + w >= WIDTH - HSTEP: # if end of line (line-wrap)
            cursor_y += font.metrics("linespace") * 1.25
            cursor_x = HSTEP  # start of row (horizontal)
      elif tok.tag == "i":
        style = "italic"
      elif tok.tag == "/i":
          style = "roman"
      elif tok.tag == "b":
          weight = "bold"
      elif tok.tag == "/b":
        weight = "normal"
    return display_list


  # helper function for scrolling
  def scroll_down(self, e):
    self.scroll += SCROLL_STEP
    self.draw()

  # function for displaying
  def draw(self):
    self.canvas.delete("all") # repainting every time
    for x, y, word, font in self.display_list:
      # optimizations for achieving 16ms (ideal animation frame budget) (1/60 second time for drawing)
      if y  > self.scroll + HEIGHT: continue  # skip render of text below (window)view
      if y + VSTEP < self.scroll : continue   # skip render of text above view
      
      self.canvas.create_text(x, y - self.scroll, text=word, font=font)

  def load(self, url):
    body = URL.request(url)
    text = lex(body)
    self.display_list = Browser.layout(text)
    self.draw()
        

if __name__ == "__main__":
  import sys
  Browser().load(URL(sys.argv[1]))
  tkinter.mainloop()