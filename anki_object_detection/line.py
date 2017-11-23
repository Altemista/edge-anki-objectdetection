class Line:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def in_area(self, x1, x2, y1, y2):
        if abs(self.y1 - y1) < 300 or abs(self.y2-y1) < 300 or abs(self.y1-y2) < 300 or abs(self.y2-y2) < 300:
            return True
        return False
