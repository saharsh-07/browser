import tkinter
import tkinter.font
from URL import *
from HTMLParser import *
from Document_Layout import *
from GLOBALS import *
from CSSParser import *
        
class Browser:
  def __init__(self):
    self.window = tkinter.Tk()
    self.canvas = tkinter.Canvas(
        self.window,
        width=WIDTH,
        height=HEIGHT,
        bg="white",
    )
    self.canvas.pack()

    self.scroll = 0
    self.window.bind("<Down>", self.scroll_down)
    self.display_list = []

  def load(self, url):
    body = url.request()
    self.nodes = HTMLParser(body).parse()
    rules = DEFAULT_STYLE_SHEET.copy()
    links = [node.attributes["href"]
             for node in tree_to_list(self.nodes, [])
             if isinstance(node, Element)
             and node.tag == "link"
             and node.attributes.get("rel") == "stylesheet"
             and "href" in node.attributes]
    for link in links:
            style_url = url.resolve(link)
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