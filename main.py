from constants import *
from block import *
from stringProcessor import *

inputStr = """
    $(3,0)[{XOR: a&.a&, b&.b& -> fg&}{AND: a&.a&, b&.b& -> fcout&}];
    $(3,0)[{XOR: cin&.cin&, fg& -> sg&^}{AND: cin&.cin&, fg& -> scout&.output&}];
    $(3,0)[{OR: fcout&, scout& -> cout&/cin(&+1).cout&#10}]
    """
inputStr2 = """$(0,3)[{CoolBlock&: a&.nameOfA&, b&.nameOfB&->c&.nameOfC&}]"""

processedString = process(inputStr2)

newBoard = Board(processedString)

newBoard.drawBoard()

