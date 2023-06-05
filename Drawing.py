from pygame import Rect, Color


class DrawingObject:
    """
    To store lines with color and thickness
    """
    color: tuple[int, int, int, int]
    start: tuple[int, int]
    end: tuple[int, int]
    thickness: int

    def __init__(self, color: tuple[int, int, int, int], start: tuple[int, int], end: tuple[int, int], thickness: int) -> None:
        self.color = color
        self.start = start
        self.end = end
        self.thickness = thickness

    
class DrawingClipboard:
    """
    Stores drawing rects to be rendered and erased.

    Singleton object, stores ALL drawing objects
    """
    lines: list[DrawingObject]

    def __init__(self) -> None:
        self.lines = []

    def addLines(self, line: DrawingObject) -> None:
        self.lines.append(line)

    def checkCollision(self, line: DrawingObject, rect: Rect) -> bool:
        
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

    def findLine(self, rect: Rect) -> list[DrawingObject]:
        """
        Find the lines that collide with <rect>
        """
        to_return = []
        for line in self.lines:
            if self.checkCollision(line, rect):
                to_return.append(line)

    def eraseAt(self, rect: Rect) -> None:
        """
        Erases the lines that collide with <rect>
        """
        for line in self.lines:
            if self.checkCollision(line, rect):
                self.lines.remove(line)


