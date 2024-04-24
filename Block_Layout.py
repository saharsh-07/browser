from GLOBALS import *
from Draw_Rect import *
from Draw_Text import *
from HTMLParser import *

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
    font = get_font(self.size, self.weight, self.style)
    w = font.measure(word)
    
    if self.cursor_x + w > self.width:  # out of view 
      self.flush()
    color = node.style["color"]
    self.line.append((self.cursor_x, word, font, color)) #making to be rendered whole line
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
                self.flush()
            for child in node.children:
                self.recurse(child)

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
      self.cursor_x = 0
      self.cursor_y = 0
      self.weight = "normal"
      self.style = "roman"
      self.size = 16
      self.line = []
      self.recurse(self.node)
      self.flush()
    
    for child in self.children:
      child.layout()
    
    if mode == "block":
      self.height = sum([child.height for child in self.children])
    else:
      self.height = self.cursor_y

  # which mode of layout it is -> inline or block
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
        x2, y2 = self.x + self.width, self.y + self.height
        rect = Draw_Rect(self.x, self.y, x2, y2, bgcolor)
        cmds.append(rect)
    for x, y, word, font, color in self.display_list:
        cmds.append(Draw_Text(self.x + x, self.y + y,
                                      word, font, color))
    return cmds
  
