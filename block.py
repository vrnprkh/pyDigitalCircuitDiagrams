from stringProcessor import *
from constants import *
from PIL import Image, ImageDraw, ImageFont
from wires import WireGrid

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
        self.displayHeight = max(self.internalHeight + V_SPACE, displayHeight) 
    
    def getBlockHeight(self): # name height + max number of ports
        return self.displayHeight

    def getRealHeight(self):
        return self.internalHeight

    def __str__(self):
        # for testing
        return f"Name: {self.name}\nInputPorts: {self.inputPorts}\nInputNames: {self.inputNames}\nOutputPorts: {self.outputPorts}\nOutputNames: {self.outputNames}\ninternalHeight: {self.internalHeight}\ndisplayHeight: {self.displayHeight}"
    def drawBlock(self, x, y, image):
        # TODO clean this
        topLeft = (x * SCALE, y * SCALE)
        bottomRight = ((x + STANDARD_WIDTH) * SCALE, (y + self.internalHeight) * SCALE )
        image.rectangle([topLeft, bottomRight], fill = BLOCK_COLOUR, outline = BLOCK_OUTLINE)

        nameFont = ImageFont.truetype("Keyboard.ttf", FONT_SIZE * 2)
        image.text(((2 * x + STANDARD_WIDTH )//2 * SCALE , y * SCALE), self.name, fill=TITLE_FONT_COLOR, anchor="ma", font=nameFont)

        font = ImageFont.truetype("Keyboard.ttf", FONT_SIZE)
        for i, e in enumerate(self.inputNames):
            eDraw = DEFAULT_PORT + e
            if filterOutString(self.inputPorts[i], ("_")) != "":
                image.text((x * SCALE + 3, (y + i + 2) * SCALE  - 3), eDraw, fill=PORT_FONT_COLOR, anchor="ls", font=font)
        for i, e in enumerate(self.outputNames):
            
            eDraw = e + DEFAULT_PORT
            if filterOutString(self.outputPorts[i], ("_")) != "":
                image.text(((x + STANDARD_WIDTH) * SCALE - 3, (y + i + 2) * SCALE - 3), eDraw, fill=PORT_FONT_COLOR, anchor="rs", font=font)

    def getInputPortPixels(self, x, y):
        return [(port, (x * SCALE, int((y + i  + 1.5) * SCALE))) for i, port in enumerate(self.inputPorts) if filterOutString(port,("_","^")) != ""]
    def getOutputPortPixels(self, x, y):
        return [(port, ((x + STANDARD_WIDTH) * SCALE, int((y + i  + 1.5) * SCALE))) for i, port in enumerate(self.outputPorts)]

        
        
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

    def getRectangles(self, x):
        y = BORDER
        rectangles = []
        for block in self.blocks:
            rectangles.append(((x * SCALE, y * SCALE), ((x + STANDARD_WIDTH) * SCALE, (y + block.getRealHeight()) * SCALE)))
            y += block.getBlockHeight()
        return rectangles

    def getAllBlocksInputPPs(self, x):
        y = BORDER
        blockInputPPs = []
        for block in self.blocks:
            blockInputPPs.append(block.getInputPortPixels(x, y))
            y += block.getBlockHeight()
        return blockInputPPs
    def getAllBlocksOutputPPs(self, x):
        y = BORDER
        blockOutputPPs = []
        for block in self.blocks:
            blockOutputPPs.append(block.getOutputPortPixels(x, y))
            y += block.getBlockHeight()
        return blockOutputPPs


class Board:
    def __init__(self, processesedStr):
        self.columns = []
        for column in processesedStr:
            self.columns.append(Column([createBlock(block) for block in column]))
        
        #board sizing
        self.width = int(len(self.columns) * (STANDARD_WIDTH + H_SPACING) * SCALE + 2 * BORDER * SCALE)
        self.height = int(max([column.getColumnHeight() for column in self.columns]) * SCALE + 2 * BORDER * SCALE)

        # useful for wire drawing
        self.rectangles = []
        x = BORDER
        for column in self.columns:
            for e in column.getRectangles(x):
                self.rectangles.append(e)
            x+= (STANDARD_WIDTH + H_SPACING)

    def drawBoard(self):
        totalWidth = self.width
        maxColumnHeight = self.height
        newImage = Image.new("RGB", (totalWidth, maxColumnHeight))
        drawNewImage = ImageDraw.Draw(newImage, "RGBA")

        drawNewImage.rectangle([(0,0), (totalWidth, maxColumnHeight)], fill=BACKGROUND)
        
        
        x = BORDER
        for column in self.columns:
            column.drawColumn(x, drawNewImage)
            x+= (STANDARD_WIDTH + H_SPACING)
            
        self.drawWires(drawNewImage)
        self.drawBadWires(drawNewImage)
        newImage.show()
    
    def findAllConnectionPixels(self):
        # takes form [portName , [(x0,y0), (x1, y1), ...]]
        filterChars = ("^", "_")
        inputCoordinates = dict()
        outputCoordinates = dict()
        x = BORDER
        for column in self.columns:
            for PPs in column.getAllBlocksInputPPs(x):
                for PP in PPs:
                    if PP[0] in inputCoordinates:
                        inputCoordinates[PP[0]].append(PP[1])
                    else:
                        inputCoordinates[PP[0]] = [PP[1],]
            
            for PPs in column.getAllBlocksOutputPPs(x):
                for PP in PPs:
                    if PP[0] in outputCoordinates:
                        outputCoordinates[PP[0]].append(PP[1])
                    else:
                        outputCoordinates[PP[0]] = [PP[1],]
            x += STANDARD_WIDTH + H_SPACING
        connections = []

        # forced IO
        
        for keyIn in inputCoordinates:
            if ((filterOutString(keyIn, filterChars) not in filterDictKeys(outputCoordinates, filterChars)) or ("^" in keyIn)) and ("_" not in keyIn):
                for inputCoord in inputCoordinates[keyIn]:
                    newLine = ((BORDER, inputCoordinates[keyIn][0][1]), inputCoord)
                    # while newLine[0][1] in [e[0][1] for e in connections if inputCoord != e[1]]:
                    #     newLine = ((newLine[0][0], newLine[0][1] + WIREPIXELS*2), newLine[1])
                    connections.append(newLine)
        
        for keyOut in outputCoordinates:
            if ((filterOutString(keyOut, filterChars) not in filterDictKeys(inputCoordinates, filterChars)) or ("^" in keyOut)) and ("_" not in keyOut):
                for outputCoord in outputCoordinates[keyOut]:
                    connections.append(((self.width - BORDER, outputCoordinates[keyOut][0][1]), outputCoord))


        # remove special nonsense
        newInputCoordinates = dict()
        newOutputCoordinates = dict()
        
        for keyIn in inputCoordinates:
            newInputCoordinates[filterOutString(keyIn, filterChars)] = inputCoordinates[keyIn]
        for keyOut in outputCoordinates:
            newOutputCoordinates[filterOutString(keyOut, filterChars)] = outputCoordinates[keyOut]

        # internal
        for keyOut in newOutputCoordinates:
            if keyOut in newInputCoordinates:
                for outputCoord in newOutputCoordinates[keyOut]:
                    for inputCoord in newInputCoordinates[keyOut]:
                        connections.append((outputCoord, inputCoord))

        
        


        return connections

    def getRailSpace(self):
        rails = [((BORDER + i * (STANDARD_WIDTH + H_SPACING)) * SCALE, (BORDER + i * STANDARD_WIDTH + (i + 1) * H_SPACING) * SCALE) for i in range(len(self.columns) - 1)]
        rails.append((0, BORDER))
        rails.append((((len(self.columns) - 1) * (STANDARD_WIDTH + H_SPACING) + BORDER) * SCALE, self.width))
        return rails

    def drawBadWires(self, drawImage):
        for e in self.findAllConnectionPixels():
            drawImage.line(e, fill=WIRECOLOR, width=WIREPIXELS)


    def drawWires(self, drawImage):
        wires = WireGrid(self.rectangles, self.findAllConnectionPixels(), self.width, self.height, WIREPIXELS, self.getRailSpace())

        