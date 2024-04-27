import tkinter
from CSSParser import *
global HEIGHT, WIDTH, HSTEP, VSTEP, SCROLL_STEP, BI_TIMES, FONTS, DEFAULT_STYLE_SHEET
global SELF_CLOSING_TAGS, HEAD_TAGS, BLOCK_ELEMENTS, get_font, paint_tree, print_tree
global tree_to_list, cascade_priority, INHERITED_PROPERTIES, style, INPUT_WIDTH_PX
global COOKIE_JAR

FONTS = {}
HEIGHT, WIDTH = 600, 800  # height and width of window
SCROLL_STEP = 100  # scroll this much scrolled using button
HSTEP, VSTEP = 13, 18 # vertical and horizontal placing delta
SELF_CLOSING_TAGS = [
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
]
HEAD_TAGS = [
        "base", "basefont", "bgsound", "noscript",
        "link", "meta", "title", "style", "script",
    ]
BLOCK_ELEMENTS = [
"html", "body", "article", "section", "nav", "aside",
"h1", "h2", "h3", "h4", "h5", "h6", "hgroup", "header",
"footer", "address", "p", "hr", "pre", "blockquote",
"ol", "ul", "menu", "li", "dl", "dt", "dd", "figure",
"figcaption", "main", "div", "table", "form", "fieldset",
"legend", "details", "summary"
]

INHERITED_PROPERTIES = {
    "font-size": "16px",
    "font-style": "normal",
    "font-weight": "normal",
    "color": "black",
}


def get_font(size, weight, slant):
    key = (size, weight, slant)
    if key not in FONTS:
        font = tkinter.font.Font(size=size, weight=weight,
        slant=slant)
        label = tkinter.Label(font=font)
        FONTS[key] = (font, label)
    return FONTS[key][0]

def paint_tree(layout_object, display_list):
    display_list.extend(layout_object.paint())

    for child in layout_object.children:
        paint_tree(child, display_list)

def print_tree(node, indent=0):
    print(" " * indent, node)
    for child in node.children:
        print_tree(child, indent + 2)

def style(node, rules):
    node.style = {}
    for property, default_value in INHERITED_PROPERTIES.items():
        if node.parent:
            node.style[property] = node.parent.style[property]
        else:
            node.style[property] = default_value
    for selector, body in rules:
        if not selector.matches(node): continue
        for property, value in body.items():
            node.style[property] = value
    from HTMLParser import Element
    if isinstance(node, Element) and "style" in node.attributes:
        pairs = CSSParser(node.attributes["style"]).body()
        for property, value in pairs.items():
            node.style[property] = value
    if node.style["font-size"].endswith("%"):
        if node.parent:
            parent_font_size = node.parent.style["font-size"]
        else:
            parent_font_size = INHERITED_PROPERTIES["font-size"]
        node_pct = float(node.style["font-size"][:-1]) / 100
        parent_px = float(parent_font_size[:-2])
        node.style["font-size"] = str(node_pct * parent_px) + "px"
    for child in node.children:
        style(child, rules)


browser_styles = open("browser.css")
DEFAULT_STYLE_SHEET = CSSParser(browser_styles.read()).parse()

def tree_to_list(tree, list):
    list.append(tree)
    for child in tree.children:
        tree_to_list(child, list)
    return list

def cascade_priority(rule):
    selector, body = rule
    return selector.priority

INPUT_WIDTH_PX = 200

COOKIE_JAR = {}