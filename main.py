from constants import *
from block import *
from stringProcessor import *

def fullBuild(inputString):
    proced = process(inputString)
    newBoard = Board(proced)
    newBoard.drawBoard()

inputStr = """
    $(3,0)[{XOR: a&.a&, b&.b& -> fg&}{AND: a&.a&, b&.b& -> fcout&}]{CIN:_->cin0};
    $(3,0)[{XOR: cin&.cin&, fg& ->_,sg&^.output&}{AND: cin&.cin&, fg& -> scout&}];
    $(3,0)[{OR: fcout&, scout& -> cin(&+1).cout&#10}]
    """
inputStr2 = """$(0,3)[{CoolBlock&: a&.nameOfA&, b&.nameOfB&->c&.nameOfC&}]"""
inputStr3 = "{NOR:S, Q2 -> Q1^}{NOR: Q1, R -> Q2^}"
fullBuild(inputStr)