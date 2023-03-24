from constants import *
from block import *
from stringProcessor import *

inputStr = "$(0,3)[{XOR: a(&), b(&) -> fg(&)}{AND: a(&), b(&) -> fcout(&)}];$(0,3)[{XOR: cin(&), fg(&) -> sg(&)^}{AND: cin(&), fg(&) -> scout(&)}];$(0,3)[{OR: fcout(&), scout(&) -> cout(&)/cin(&+1)#10}]"
processedString = process(inputStr)

newBoard = Board(processedString)

newBoard.drawBoard()

