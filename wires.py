# implementation for a wire drawing alg
# steps: create a list of rectangles that are off limits, (with padding)
# generate rails 
# assign a output to a set of rails
# 

class Rail:
    def __init__(self, top, bottom):
        self.top = top
        self.bottom = bottom
        self.isOccupied = False
        self.occupant = ""
        self.links = [] #ints
    
    def occupy(self, outputPort):
        self.isOccupied = True
        self.occupant = outputPort

    def shrink(self):
        # returns a new rail after shrinking itself
        newTop = min(self.links)
        newBottom = max(self.links)
        self.top = newTop
        self.bottom = newBottom

    
    def size(self):
        return self.bottom - self.top


class WireGrid:
    def __init__(self, rectangles, connectionGoals, boardWidth, boardHeight, wireSize, railSpace):
        self.rectangles = rectangles
        self.wires = []
        self.connectionGoals = connectionGoals
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.wireSize = wireSize
        self.railSpace = railSpace
        
        self.rails = []
        self.generateRails()

        self.createWires()


    def generateRails(self):
        pass

    def createWires(self):
        pass