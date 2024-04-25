from Rect import *
from GLOBALS import *
from Draw_Rect import *
from Draw_Line import *
from Draw_Outline import *
from Draw_Text import *
from URL import *


class Chrome:
  """
  Real web browsers don’t just show web page contents—they’ve got labels 
  and icons and buttons.Oh my! This is called the browser “chrome”;
  Yep, that predates and inspired the name of Google’s Chrome browser. a
  ll of this stuff is drawn by the browser to the same window as the page contents,
  and it requires information about the browser as a whole (like the list of all tabs),
  so it has to happen at the browser level, not per-tab.
  """
  def __init__(self, browser):
        self.browser = browser
        self.font = get_font(16, "normal", "roman")
        self.font_height = self.font.metrics("linespace")
        self.padding = 5
        self.tabbar_top = 0
        self.tabbar_bottom = self.font_height + 2*self.padding
        plus_width = self.font.measure("+") + 2*self.padding
        self.newtab_rect = Rect(
           self.padding, self.padding,
           self.padding + plus_width,
           self.padding + self.font_height)
        self.bottom = self.tabbar_bottom
        self.urlbar_top = self.tabbar_bottom
        self.urlbar_bottom = self.urlbar_top + \
            self.font_height + 2*self.padding
        self.bottom = self.urlbar_bottom
        back_width = self.font.measure("<") + 2*self.padding
        self.back_rect = Rect(
            self.padding,
            self.urlbar_top + self.padding,
            self.padding + back_width,
            self.urlbar_bottom - self.padding)

        self.address_rect = Rect(
            self.back_rect.top + self.padding,
            self.urlbar_top + self.padding,
            WIDTH - self.padding,
            self.urlbar_bottom - self.padding)
        self.focus = None
        self.address_bar = ""

  
  def tab_rect(self, i):
        tabs_start = self.newtab_rect.right + self.padding
        tab_width = self.font.measure("Tab X") + 2*self.padding
        return Rect(
            tabs_start + tab_width * i, self.tabbar_top,
            tabs_start + tab_width * (i + 1), self.tabbar_bottom)
  
  def paint(self):
        cmds = []
        cmds.append(Draw_Rect(
            Rect(0, 0, WIDTH, self.bottom),
            "white"))
        cmds.append(Draw_Line(
            0, self.bottom, WIDTH,
            self.bottom, "black", 1))

        cmds.append(Draw_Outline(self.newtab_rect, "black", 1))
        cmds.append(Draw_Text(
            self.newtab_rect.left + self.padding,
            self.newtab_rect.top,
            "+", self.font, "black"))

        for i, tab in enumerate(self.browser.tabs):
            bounds = self.tab_rect(i)
            cmds.append(Draw_Line(
                bounds.left, 0, bounds.left, bounds.bottom,
                "black", 1))
            cmds.append(Draw_Line(
                bounds.right, 0, bounds.right, bounds.bottom,
                "black", 1))
            cmds.append(Draw_Text(
                bounds.left + self.padding, bounds.top + self.padding,
                "Tab {}".format(i), self.font, "black"))

            if tab == self.browser.active_tab:
                cmds.append(Draw_Line(
                    0, bounds.bottom, bounds.left, bounds.bottom,
                    "black", 1))
                cmds.append(Draw_Line(
                    bounds.right, bounds.bottom, WIDTH, bounds.bottom,
                    "black", 1))

        cmds.append(Draw_Outline(self.back_rect, "black", 1))
        cmds.append(Draw_Text(
            self.back_rect.left + self.padding,
            self.back_rect.top,
            "<", self.font, "black"))

        cmds.append(Draw_Outline(self.address_rect, "black", 1))
        if self.focus == "address bar":
            cmds.append(Draw_Text(
                self.address_rect.left + self.padding,
                self.address_rect.top,
                self.address_bar, self.font, "black"))
            w = self.font.measure(self.address_bar)
            cmds.append(Draw_Line(
                self.address_rect.left + self.padding + w,
                self.address_rect.top,
                self.address_rect.left + self.padding + w,
                self.address_rect.bottom,
                "red", 1))
        else:
            url = str(self.browser.active_tab.url)
            cmds.append(Draw_Text(
                self.address_rect.left + self.padding,
                self.address_rect.top,
                url, self.font, "black"))

        return cmds

  def click(self, x, y):
    self.focus = None
    if self.newtab_rect.containsPoint(x, y):
        self.browser.new_tab(URL("https://browser.engineering/"))
    elif self.back_rect.containsPoint(x, y):
        self.browser.active_tab.go_back()
    elif self.address_rect.containsPoint(x, y):
        self.focus = "address bar"
        self.address_bar = ""
    else:
        for i, tab in enumerate(self.browser.tabs):
            if self.tab_rect(i).containsPoint(x, y):
                self.browser.active_tab = tab
                break

  def keypress(self, char):
        if self.focus == "address bar":
            self.address_bar += char
  
  def enter(self):
        if self.focus == "address bar":
            self.browser.active_tab.load(URL(self.address_bar))
            self.focus = None