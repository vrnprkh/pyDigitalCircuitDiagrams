from stringProcessor import *


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



class Column:
    def __init__(self, blockStrings):
        self.blocks = []
        for blockString in blockStrings:
            self.addBlockStringToBlocks(blockString)


    def addBlockStringToBlocks(self, blockString):
        self.blocks.append(createBlock(blockString))


class Boards:
    def __init(self, columns):
        self.columns = columns

        