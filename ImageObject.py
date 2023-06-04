from pygame import Surface, Rect


class ImageObject():
    """
    Stores images to be rendered and moved
    """

    def __init__(self, image: Surface, pos: tuple[int, int]) -> None:
        self.image = image
        self.pos = image.get_rect().move([pos[0], pos[1]])

    def __repr__(self) -> str:
        return f"{self.pos.center}"

    def move(self, pos: tuple[int, int]):
        self.pos.move_ip(pos[0], pos[1])

    def get_rect(self) -> Rect:
        return self.pos
