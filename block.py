from stringProcessor import *
from constants import *
from PIL import Image, ImageDraw, ImageFont


#TODO move this to object
def createBlock(blockString):
    assert(validBlock(blockString))
    nameSep = findAllStrings(blockString, ":")
    if len(nameSep) == 1:
        name = blockString[:nameSep[0]]
    else:
        name = ""
    nameLess = ""
    if len(nameSep) == 1:
        nameLess += blockString[nameSep[0] + 1:]
    else:
        nameLess += blockString
    
    virtualHeightSep = findAllStrings(nameLess, "#")
    
    nameHeightLess = ""
    if len(virtualHeightSep) == 1:
        nameHeightLess += nameLess[:virtualHeightSep[0]]
        height = int(nameLess[virtualHeightSep[0] + 1:])
    else:
        nameHeightLess += nameLess
        height = 0
    
    splitIO = nameHeightLess.split("->")
    inputs = splitIO[0].split(",")
    outputs = splitIO[1].split(",")
    inputPorts = []
    inputNames = []
    outputPorts = []
    outputNames = []
    for i in inputs:
        if "." in i:
            inputPorts.append(i.split(".")[0])
            inputNames.append(i.split(".")[1])
        else:
            inputPorts.append(i)
            inputNames.append("")
    for o in outputs:
        if "." in o:
            outputPorts.append(o.split(".")[0])
            outputNames.append(o.split(".")[1])
        else:
            outputPorts.append(o)
            outputNames.append("")

    returnBlock = Block(name, inputPorts, inputNames, outputPorts, outputNames, height)
    return returnBlock

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
        self.displayHeight = max(self.internalHeight+ V_SPACE, displayHeight) 
    
    def getBlockHeight(self): # name height + max number of ports
        return self.displayHeight

    def __str__(self):
        return f"Name: {self.name}\nInputPorts: {self.inputPorts}\nInputNames: {self.inputNames}\nOutputPorts: {self.outputPorts}\nOutputNames: {self.outputNames}\ninternalHeight: {self.internalHeight}\ndisplayHeight: {self.displayHeight}"
    def drawBlock(self, x, y, image):
        topLeft = (x * SCALE, y * SCALE)
        bottomRight = ((x + STANDARD_WIDTH) * SCALE, (y + self.internalHeight) * SCALE )
        image.rectangle([topLeft, bottomRight], fill = BLOCK_COLOUR, outline = BLOCK_OUTLINE)

        nameFont = ImageFont.truetype("Keyboard.ttf", FONT_SIZE * 2)
        image.text(((2 * x + STANDARD_WIDTH )//2 * SCALE , y * SCALE), self.name, fill="black", anchor="ma", font=nameFont)


        font = ImageFont.truetype("Keyboard.ttf", FONT_SIZE)
        for i, e in enumerate(self.inputNames):
            image.text((x * SCALE + 3, (y + i + 2) * SCALE  - 3), e, fill="black", anchor="ls", font=font)
        for i, e in enumerate(self.outputNames):
            image.text(((x + STANDARD_WIDTH) * SCALE - 3, (y + i + 2) * SCALE - 3), e, fill="black", anchor="rs", font=font)

        
        
class Column:
    def __init__(self, blocks):
        self.blocks = blocks
    
    def getColumnHeight(self):
        return sum([block.getBlockHeight() for block in self.blocks])
        
    def drawColumn(self, x, image):
        y = BORDER
        for block in self.blocks:
            block.drawBlock(x, y, image)
            y += block.getBlockHeight()

class Board:
    def __init__(self, processesedStr):
        self.columns = []
        for column in processesedStr:
            self.columns.append(Column([createBlock(block) for block in column]))


    def drawBoard(self):
        totalWidth = int(len(self.columns) * (STANDARD_WIDTH + H_SPACING) * SCALE + 2 * BORDER * SCALE)
        maxColumnHeight = int(max([column.getColumnHeight() for column in self.columns]) * SCALE + 2 * BORDER * SCALE)
        newImage = Image.new("RGB", (totalWidth, maxColumnHeight))
        drawNewImage = ImageDraw.Draw(newImage)

        drawNewImage.rectangle([(0,0), (totalWidth, maxColumnHeight)], fill=BACKGROUND)
        
        
        x = BORDER
        for column in self.columns:
            column.drawColumn(x, drawNewImage)
            x+= (STANDARD_WIDTH + H_SPACING)
        
        newImage.show()
        

        