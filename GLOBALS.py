import tkinter
global HEIGHT, WIDTH, HSTEP, VSTEP, SCROLL_STEP, BI_TIMES, FONTS 
global SELF_CLOSING_TAGS, HEAD_TAGS, BLOCK_ELEMENTS, get_font, paint_tree, print_tree

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