from constants import *
from block import *
from stringProcessor import *

inputStr = """
    $(3,0)[{XOR: a&.a&, b&.b& -> fg&}{AND: a&.a&, b&.b& -> fcout&}];
    $(3,0)[{XOR: cin&.cin&, fg& -> sg&^}{AND: cin&.cin&, fg& -> scout&.output&}];
    $(3,0)[{OR: fcout&, scout& -> cout&/cin(&+1).cout&#10}]"""
processedString = process(inputStr)

newBoard = Board(processedString)

newBoard.drawBoard()

