from constants import *
from block import *
from stringProcessor import *

def fullBuild(inputString):
    newBoard = Board(process(inputString))
    newBoard.drawBoard()

inputStr = """
    $(3,0)[{XOR: a&.a&, b&.b& -> fg&}{AND: a&.a&, b&.b& -> fcout&}];
    $(3,0)[{XOR: cin&.cin&, fg& -> sg&^}{AND: cin&.cin&, fg& -> scout&^.output&}];
    $(3,0)[{OR: fcout&, scout& -> cin(&+1).cout&#10}]
    """
inputStr2 = """$(0,3)[{CoolBlock&: a&.nameOfA&, b&.nameOfB&->c&.nameOfC&}]"""

fullBuild(inputStr)