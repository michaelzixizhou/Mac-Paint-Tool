from pygame import Color, Rect
from typing import Union


class DrawingObject():
    """
    To be inherited from
    """

    def __init__(self) -> None:
        pass


class DrawingLine():
    """
    To store lines with color, start pos, end pos, and thickness
    """
    color: Union[tuple[int, int, int, int], Color]
    start: tuple[int, int]
    end: tuple[int, int]
    thickness: int

    def __init__(self, color: Union[tuple[int, int, int, int], Color], start: tuple[int, int], end: tuple[int, int], thickness: int) -> None:
        self.color = color
        self.start = start
        self.end = end
        self.thickness = thickness

    def __repr__(self) -> str:
        return f"Line from {self.start} to {self.end}"


# class DrawingDot():
#     """
#     To store dots with color, radius, center
#     """
#     color: tuple[int, int, int, int]
#     center: tuple[int, int]
#     radius: int

#     def __init__(self, color: tuple[int, int, int, int], center: tuple[int, int], radius: int) -> None:
#         self.color = color
#         self.center = center
#         self.radius = radius

#     def __repr__(self) -> str:
#         return f"Dot at {self.center}"

    
class DrawingClipboard():
    """
    Stores drawing rects to be rendered and erased.

    Singleton object, stores ALL drawingObjects
    """
    objs: list[DrawingLine]

    def __init__(self) -> None:
        self.objs = []

    def addLines(self, line: DrawingLine) -> None:
        self.objs.append(line)

    def check_collision_line(self, line: DrawingLine, rect: Rect) -> bool:
        """
        Check if <rect> collides with any lines
        """
        if line.start[0] < line.end[0]:
            x1, y1 = line.start[0], line.start[1]
            x2, y2 = line.end[0], line.end[1]
        else:
            x1, y1 = line.end[0], line.end[1]
            x2, y2 = line.start[0], line.start[1]
            
        try:
            slope = (y2 - y1) / (x2 - x1)
            b = y1 - (slope * x1) 
            
            while x1 < x2:
                y = (slope * x1) + b
                if rect.collidepoint(x1, y):
                    return True
                x1 += 1

        except ZeroDivisionError: # Horizontal line
            if y1 < y2:
                start, end = y1, y2
            else:
                start, end = y2, y1
            
            while start < end:
                if rect.collidepoint(x1, start):
                    return True
                start += 1
        
        return False
    
    # def check_collision_dot(self, dot: DrawingDot, rect: Rect) -> bool:
    #     """
    #     Check if rect collides with <dot>
    #     """
    #     h, k = dot.center
    #     r = dot.radius
        
    #     for x in range(h - r, h + r + 1):
    #         for y in range(k - r, k + r + 1):
    #             if rect.collidepoint(x, y):
    #                 return True
                
    #     return False
    
    def find_collision(self, obj, rect: Rect) -> bool:
        if isinstance(obj, DrawingLine):
            return self.check_collision_line(obj, rect)
        # elif isinstance(obj, DrawingDot):
        #     return self.check_collision_dot(obj, rect)
        return False

    def findLine(self, rect: Rect) -> list[DrawingLine]:
        """
        Find the lines that collide with <rect>
        """
        to_return = []
        for obj in self.objs:
            if self.find_collision(obj, rect):
                to_return.append(obj)
        return to_return

    def eraseAt(self, rect: Rect) -> None:
        """
        Erases the lines that collide with <rect>
        """
        for obj in self.objs:
            if self.find_collision(obj, rect):
                self.objs.remove(obj)

    def clearBoard(self) -> None:
        """
        Clears all lines
        """
        self.objs = []

