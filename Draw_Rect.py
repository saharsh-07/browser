class Draw_Rect:
  def __init__(self, x1, y1, x2, y2, color):
    self.top = y1
    self.left = x1
    self.bottom = y2
    self.right = x2
    self.color = color
    
  def execute(self, scroll, canvas):
    canvas.create_rectangle(
    self.left, self.top - scroll,
    self.right, self.bottom - scroll,
    width=0,
    fill=self.color)


  def __repr__(self):
    return "DrawRect(top={} left={} bottom={} right={} color={})".format(
        self.top, self.left, self.bottom, self.right, self.color)
