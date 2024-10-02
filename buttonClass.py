import uiClass

class Button(uiClass.uiObject):
    def __init__(self, x: int, y: int, width: int, height: int, name: str, func, text: str, type: str, bg_color: tuple[int, int, int] = None, scale: int = 1, top_left: tuple[int, int] = None, middle_top: tuple[int, int] = None):
        self.type = type
        super().__init__(x, y, width, height, name, scale, text=text, bg_color=bg_color, func=func)
        if top_left:
            self.rect.topleft = top_left
        if middle_top:
            self.rect.midtop = middle_top
        
