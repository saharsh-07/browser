import tkinter
import tkinter.font
from URL import *
from HTMLParser import *
from Document_Layout import *
from GLOBALS import *
from CSSParser import *
        
class Tab:
  def __init__(self, tab_height):
    self.url = None
    self.history = []
    self.tab_height = tab_height

  def load(self, url):
    body = url.request()
    self.scroll = 0
    self.history.append(url)
    self.url = url
    self.nodes = HTMLParser(body).parse()

    rules = DEFAULT_STYLE_SHEET.copy()
    links = [node.attributes["href"]
             for node in tree_to_list(self.nodes, [])
             if isinstance(node, Element)
             and node.tag == "link"
             and node.attributes.get("rel") == "stylesheet"
             and "href" in node.attributes]
    for link in links:
            try:
                body = style_url.request()
            except:
                continue
            rules.extend(CSSParser(body).parse())
    style(self.nodes, sorted(rules, key=cascade_priority))
    
    self.document = Document_Layout(self.nodes)
    self.document.layout()  # making layout document tree
    self.display_list = []
    paint_tree(self.document, self.display_list)


  # function for displaying
  def draw(self, canvas, offset):
        for cmd in self.display_list:
            if cmd.rect.top > self.scroll + self.tab_height: continue
            if cmd.rect.bottom < self.scroll: continue
            cmd.execute(self.scroll - offset, canvas)

  # helper function for scrolling
  def scroll_down(self):
        max_y = max(
            self.document.height + 2*VSTEP - self.tab_height, 0)
        self.scroll = min(self.scroll + SCROLL_STEP, max_y)

  def go_back(self):
        if len(self.history) > 1:
            self.history.pop()
            back = self.history.pop()
            self.load(back)

  def click(self, x, y):
    y += self.scroll 
    objs = [obj for obj in tree_to_list(self.document, [])
        if obj.x <= x < obj.x + obj.width
        and obj.y <= y < obj.y + obj.height]
    if not objs: return
    elt = objs[-1].node
    while elt:
      if isinstance(elt, Text):
          pass
      elif elt.tag == "a" and "href" in elt.attributes:
        url = self.url.resolve(elt.attributes["href"])
        return self.load(url)
      elt = elt.parent
    