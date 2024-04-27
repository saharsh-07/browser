import tkinter
import tkinter.font
from URL import *
from HTMLParser import *
from Document_Layout import *
from GLOBALS import *
from CSSParser import *
from JS_Context import *
import urllib
import dukpy

class Tab:
  def __init__(self, tab_height):
    self.url = None
    self.history = []
    self.tab_height = tab_height
    self.focus = None

  def load(self, url, payload=None):
        self.scroll = 0
        self.url = url
        self.history.append(url)
        body = url.request(payload)
        self.nodes = HTMLParser(body).parse()
        scripts = [node.attributes["src"] for node
                   in tree_to_list(self.nodes, [])
                   if isinstance(node, Element)
                   and node.tag == "script"
                   and "src" in node.attributes]
        self.js = JS_Context(self)
        for script in scripts:
            body = url.resolve(script).request()
            try:
                self.js.run(body)
            except dukpy.JSRuntimeError as e:
                print("Script", script, "crashed", e)

        self.rules = DEFAULT_STYLE_SHEET.copy()
        links = [node.attributes["href"]
                 for node in tree_to_list(self.nodes, [])
                 if isinstance(node, Element)
                 and node.tag == "link"
                 and node.attributes.get("rel") == "stylesheet"
                 and "href" in node.attributes]
        for link in links:
            try:
                body = url.resolve(link).request()
            except:
                continue
            self.rules.extend(CSSParser(body).parse())

        self.render()

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

  def render(self):
        style(self.nodes, sorted(self.rules, key=cascade_priority))
        self.document = Document_Layout(self.nodes)
        self.document.layout()
        self.display_list = []
        paint_tree(self.document, self.display_list)

  def go_back(self):
        if len(self.history) > 1:
            self.history.pop()
            back = self.history.pop()
            self.load(back)

  def keypress(self, char):
        if self.focus:
            if self.js.dispatch_event("keydown", self.focus): return
            self.focus.attributes["value"] += char
            self.render()

  def click(self, x, y):
    self.focus = None
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
            if self.js.dispatch_event("click", elt): return
            url = self.url.resolve(elt.attributes["href"])
            return self.load(url)
        elif elt.tag == "input":
            if self.js.dispatch_event("click", elt): return
            elt.attributes["value"] = ""
            if self.focus:
                self.focus.is_focused = False
            self.focus = elt
            elt.is_focused = True
            return self.render()
        elif elt.tag == "button":
            if self.js.dispatch_event("click", elt): return 
            while elt:
                if elt.tag == "form" and "action" in elt.attributes:
                    return self.submit_form(elt)
                elt = elt.parent
        elt = elt.parent

  def submit_form(self, elt):
        if self.js.dispatch_event("submit", elt): return
        inputs = [node for node in tree_to_list(elt, [])
                  if isinstance(node, Element)
                  and node.tag == "input"
                  and "name" in node.attributes]
        body = ""
        for input in inputs:
            name = input.attributes["name"]
            value = input.attributes.get("value", "")
            name = urllib.parse.quote(name)
            value = urllib.parse.quote(value)
            body += "&" + name + "=" + value
        body = body[1:]
        url = self.url.resolve(elt.attributes["action"])
        self.load(url, body)