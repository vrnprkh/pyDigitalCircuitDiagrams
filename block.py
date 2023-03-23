from stringProcessor import *
from constants import *



class Block:
    def __init__(self, name, inputPorts, inputNames, outputPorts, outputNames, displayHeight):
        #pre
        assert(len(inputPorts) == len(inputNames))
        assert(len(outputPorts) == len(outputNames))
        self.name = name
        self.inputPorts = inputPorts
        self.inputNames = inputNames
        self.outputPorts = outputPorts
        self.outputNames = outputNames
        self.internalHeight = 1 + max(len(inputPorts), len(outputPorts))
        self.displayHeight = displayHeight
    
    def getHeight(self): # name height + max number of ports
        return self.displayHeight

    def __str__(self):
        return f"Name: {self.name}\nInputPorts: {self.inputPorts}\nInputNames: {self.inputNames}\nOutputPorts: {self.outputPorts}\nOutputNames: {self.outputNames}\ninternalHeight: {self.internalHeight}\ndisplayHeight: {self.displayHeight}"
    def draw(self, x, y):
        topLeft = x * SCALE, y * SCALE
        bottomRight = (x + STANDARD_WIDTH) * SCALE, (y + self.internalHeight) * SCALE 
        
        



class Column:
    def __init__(self, blockStrings):
        self.blocks = []
        for blockString in blockStrings:
            self.addBlockStringToBlocks(blockString)
    
    def addBlockStringToBlocks(self, blockString):
        newBlock = createBlock(blockString)
        self.blocks.append(newBlock)



class Board:
    def __init(self, columns):
        self.columns = columns

        