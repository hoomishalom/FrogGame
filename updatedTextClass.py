import uiClass


class updatedTextObject(uiClass.uiObject):
    def __init__(
        self,
        x: int,
        y: int,
        name: str,
        scale: float,
        text: str,
        bg_color: tuple[int, int, int] = None,
        start_value: str = None
    ):
        super().__init__(x, y, 0, 0, name, scale, text, bg_color, type="updated_text")
        self.start_value = start_value
        self.type = "updated_text"
        self.display_text = self.MAIN_FONT.render(
            f"{self.text}: {self.start_value}", False, (0, 0, 0)
            # , self.bg_color
        )


    def update(self, updated_variable=None):
        self.display_text = self.MAIN_FONT.render(
            f"{self.text}: {updated_variable}", False, (0, 0, 0)
            # , self.bg_color
        )
