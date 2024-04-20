from GLOBALS import *
import tkinter, tkinter.font
from Browser import Tag, Text


# page coordination layouting
class Layout:
  def __init__(self, tokens):
    self.display_list = []
    self.cursor_x = HSTEP
    self.cursor_y = VSTEP
    self.weight = "normal"
    self.style = "roman"
    for tok in tokens:
        self.token(tok)
    
  def token(self, tok):
    # font = tkinter.font.Font() 
    if isinstance(tok, Text):
      for word in tok.text.split():
        self.word(word)
    elif tok.tag == "i":
      style = "italic"
    elif tok.tag == "/i":
      style = "roman"
    elif tok.tag == "b":
      weight = "bold"
    elif tok.tag == "/b":
      weight = "normal"
    return self.display_list

  def word(self, word):
    font = tkinter.font.Font(
              size=16,
              weight=self.weight,
              slant=self.style,
          )
    w = font.measure(word)
    self.display_list.append((self.cursor_x, self.cursor_y, word, font)) # horizontal, vertical delta, characters in text
    self.cursor_x += w + font.measure(" ") # keep displaying with diff of horiz delta
    if self.cursor_x + w >= WIDTH - HSTEP: # if end of line (line-wrap)
      self.cursor_y += font.metrics("linespace") * 1.25
      self.cursor_x = HSTEP  # start of row (horizontal)