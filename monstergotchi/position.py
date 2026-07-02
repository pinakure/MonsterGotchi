class Position:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def getScaled(self, scale):
        return Position(int(self.x*scale), int(self.y*scale))
    
    def copy(self):
        return Position( self.x, self.y )
        
    def set(self, x, y):
        self.x = x
        self.y = y
        