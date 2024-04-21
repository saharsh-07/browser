global HEIGHT, WIDTH, HSTEP, VSTEP, SCROLL_STEP, BI_TIMES, FONTS, SELF_CLOSING_TAGS, HEAD_TAGS

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