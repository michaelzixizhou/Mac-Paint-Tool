from pygame import Surface, Rect


class ImageObject():
    """
    Stores images to be rendered and moved
    """
    image: Surface
    rect: Rect

    def __init__(self, image: Surface, pos: tuple[int, int]) -> None:
        self.image = image
        self.rect = image.get_rect().move([pos[0], pos[1]])

    def __repr__(self) -> str:
        return f"{self.rect.center}"

    def move(self, pos: tuple[int, int]):
        self.rect.move_ip(pos[0], pos[1])

    def get_rect(self) -> Rect:
        return self.rect
