class Line_Layout:
    def __init__(self, node, parent, previous):
        self.node = node
        self.parent = parent
        self.previous = previous
        self.children = []

    def layout(self):
      self.width = self.parent.width
      self.x = self.parent.x

      if self.previous:
          self.y = self.previous.y + self.previous.height
      else:
          self.y = self.parent.y
      
      for word in self.children:
            word.layout()
      
      if not self.children:
            self.height = 0
            return

      max_ascent = max([word.font.metrics("ascent") for word in self.children])
      baseline = self.y + 1.25 * max_ascent
      for word in self.children:
          word.y = baseline - word.font.metrics("ascent")
      max_descent = max([word.font.metrics("descent")
                        for word in self.children])
      self.height = 1.25 * (max_ascent + max_descent)
    
    def paint(self):
      return []
