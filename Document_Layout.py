from Block_Layout import *
from GLOBALS import *

class Document_Layout:  # whole document representatiion tree 
  def __init__(self, node):
    self.node = node
    self.parent = None  
    self.previous = None
    self.children = []

  def layout(self):
    child = Block_Layout(self.node, self, None) # get children of the node 
    self.children.append(child)
    self.width = WIDTH - 2*HSTEP
    self.x = HSTEP  # layout w.r.t. x and y coordi
    self.y = VSTEP
    child.layout()  # recurse until leaf node(eg. body -> div -> p)
    self.height = child.height

  def paint(self):
    return [] # nothing for doc to paint as block does that

  def __repr__(self):
    return "DocumentLayout()"
