class Tag_Selector:
    def __init__(self, tag):
        self.tag = tag
        self.priority = 1

    def matches(self, node):
      from HTMLParser import Element
      return isinstance(node, Element) and self.tag == node.tag
