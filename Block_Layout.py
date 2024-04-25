from GLOBALS import *
from Draw_Rect import *
from Draw_Text import *
from HTMLParser import *
from Line_Layout import *
from Text_Layout import *
from Draw_Line import *
from Draw_Rect import *
from Rect import *

class Block_Layout:
  # Block will need below parameters for tree building
  def __init__(self, node, parent, previous):
    self.node = node
    self.parent = parent
    self.previous = previous
    self.children = []
    self.x = None # default layout of coordi
    self.y = None
    self.width = None
    self.height = None
    self.display_list = []

  # tokenization
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

  # word formatting
  def word(self, node, word):
    weight = node.style["font-weight"]
    style = node.style["font-style"]
    if style == "normal": style = "roman"
    size = int(float(node.style["font-size"][:-2]) * .75)
    font = get_font(size, weight, style)
    w = font.measure(word)
    
    if self.cursor_x + w > self.width:  # out of view 
      self.new_line()
    line = self.children[-1]
    previous_word = line.children[-1] if line.children else None
    text = Text_Layout(node, word, line, previous_word)
    line.children.append(text)
    self.cursor_x += w + font.measure(" ") # keep displaying with diff of horiz delta

  # processing buffer of tree nodes
  def flush(self):
    if not self.line: return
    metrics = [font.metrics() for x, word, font, color in self.line]
    max_ascent = max([metric["ascent"] for metric in metrics])
    baseline = self.cursor_y + 1.25 * max_ascent
    for x, word, font, color in self.line:
        y = baseline - font.metrics("ascent")
        self.display_list.append((x, y, word, font, color))
    self.cursor_x = self.x
    self.line = []
    max_descent = max([metric["descent"] for metric in metrics])
    self.cursor_y = baseline + 1.25 * max_descent


  def recurse(self, node):
        if isinstance(node, Text):
            for word in node.text.split():
                self.word(node, word)
        else:
            if node.tag == "br":
                self.new_line()
            for child in node.children:
                self.recurse(child)
  def new_line(self):
    self.cursor_x = 0
    last_line = self.children[-1] if self.children else None
    new_line = Line_Layout(self.node, self, last_line)
    self.children.append(new_line)
    
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
  
  # making tree layout of the block
  def layout(self):
    self.x = self.parent.x
    self.width = self.parent.width
    
    if self.previous:
      self.y = self.previous.y + self.previous.height
    else:
      self.y = self.parent.y
    
    mode = self.layout_mode()
    
    if mode == "block":
      previous = None
    
      for child in self.node.children:
        next = Block_Layout(child, self, previous)
        self.children.append(next)
        previous = next
    
    else:
      self.new_line()
      self.recurse(self.node)
    
    for child in self.children:
      child.layout()

    self.height = sum([child.height for child in self.children])
  
  def layout_mode(self):
    if isinstance(self.node, Text):
      return "inline"
    elif any([isinstance(child, Element) and \
      child.tag in BLOCK_ELEMENTS
      for child in self.node.children]):
      return "block"
    elif self.node.children:
      return "inline"
    else:
      return "block"
  
  # draw either rectangle or text into document
  def paint(self):
    cmds = []
    bgcolor = self.node.style.get("background-color",
                                  "transparent")
    if bgcolor != "transparent":
        rect = Draw_Rect(self.self_rect(), bgcolor)
        cmds.append(rect)
    return cmds

    return cmds
  
  def self_rect(self):
        return Rect(self.x, self.y,
            self.x + self.width, self.y + self.height)