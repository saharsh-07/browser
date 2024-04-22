class Draw_Text:
  def __init__(self, x1, y1, text, font):
      self.top = y1
      self.left = x1
      self.text = text
      self.font = font
      self.bottom = y1 + font.metrics("linespace")

  def execute(self, scroll, canvas):
    canvas.create_text(
      self.left, self.top - scroll,
      text=self.text,
      font=self.font,
      anchor='nw')

  def __repr__(self):
    return "DrawText(top={} left={} bottom={} text={} font={})".format(
        self.top, self.left, self.bottom, self.text, self.font)