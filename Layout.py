from GLOBALS import *
import tkinter, tkinter.font
from Browser import Element, Text


# page coordination layouting
class Layout:
  def __init__(self, tree):
    self.display_list = []

    self.cursor_x = HSTEP
    self.cursor_y = VSTEP
    self.weight = "normal"
    self.style = "roman"
    self.size = 16
    
    self.line = []
    self.recurse(tree)
    self.flush()
  

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
    elif tok.tag == "small":
      self.size -= 2
    elif tok.tag == "/small":
      self.size += 2
    elif tok.tag == "big":
      self.size += 4
    elif tok.tag == "/big":
      self.size -= 4
    elif tok.tag == "br":
      self.flush()
    elif tok.tag == "/p":
      self.flush()
      self.cursor_y += VSTEP


  def word(self, word):
    font = self.get_font(self.size, self.weight, self.style)
    w = font.measure(word)
    if self.cursor_x + w > WIDTH - HSTEP:
      self.flush()
    self.line.append((self.cursor_x, word, font))
    self.cursor_x += w + font.measure(" ") # keep displaying with diff of horiz delta
    
  def flush(self):
    if not self.line: return
    metrics = [font.metrics() for x, word, font in self.line]
    max_ascent = max([metric["ascent"] for metric in metrics])
    baseline = self.cursor_y + 1.25 * max_ascent
    for x, word, font in self.line:
      y = baseline - font.metrics("ascent")
      self.display_list.append((x, y, word, font))
    max_descent = max([metric["descent"] for metric in metrics])
    self.cursor_y = baseline + 1.25 * max_descent
    self.cursor_x = HSTEP
    self.line = []



  def recurse(self, tree):
    if isinstance(tree, Text):
      for word in tree.text.split():
        self.word(word)
    else:
      self.open_tag(tree.tag)
      for child in tree.children:
        self.recurse(child)
      self.close_tag(tree.tag)

  def get_font(self, size, weight, slant):
    key = (size, weight, slant)
    if key not in FONTS:
      font = tkinter.font.Font(size=size, weight=weight,
        slant=slant)
      label = tkinter.Label(font=font)
      FONTS[key] = (font, label)
    return FONTS[key][0]


  def open_tag(self, tag):
    if tag == "i":
      self.style = "italic"
    elif tag == "b":
      self.weight = "bold"
    elif tag == "small":
      self.size -= 2
    elif tag == "big":
      self.size += 4
    elif tag == "br":
      self.flush()


  def close_tag(self, tag):
    if tag == "i":
      self.style = "roman"
    elif tag == "b":
      self.weight = "normal"
    elif tag == "small":
      self.size += 2
    elif tag == "big":
      self.size -= 4
    elif tag == "p":
      self.flush()
      self.cursor_y += VSTEP

