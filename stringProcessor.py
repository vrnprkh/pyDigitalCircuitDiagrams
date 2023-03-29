# format strings
# 1. remove all whitespace
# 2. split by column
# 3. check validity for each column
# 4. remap any shorthands
# 5. expand iterators
# 6. return list of blocks


def removeWhitespace(inputString):
    returnString = ""
    for e in inputString:
        if (e != " ") and (e != "\n"):
            returnString += e
    return returnString

# for split just use built in

# returns the index of each substring that is in desired string
def findAllStrings(anyString, searchString):
    return [i for i in range(len(anyString) - len(searchString) + 1) if anyString[i:i+len(searchString)] == searchString]



# checks that there are the same number of $, [, and ], and their posistion is correct
def checkIteratorSplit(columnString):
    iteratorStarts = findAllStrings(columnString, "$")
    iteratorOpen = findAllStrings(columnString, "[")
    iteratorClose = findAllStrings(columnString, "]")
    if len(iteratorStarts) < 1 and (len(iteratorOpen) > 0):
        return False
    if not (len(iteratorOpen) == len(iteratorClose)):
        print("Iterator split error due to unbalanced iterator starts: $, or iterator brackets: [, ]")
        return False
    for i in range(len(iteratorOpen)):
        if not (iteratorOpen[i] < iteratorClose[i]):
            print("Iterator split error due to misplaced iterator brackets, i.e $][")
            return False
    return True

# splits a column into iterators, by finding dollar signs for start, and ] for ends
def splitColumnToIterator(columnString):
    # pre
    assert(checkIteratorSplit(columnString))

    iteratorStarts = findAllStrings(columnString, "$")
    iteratorClose = findAllStrings(columnString, "]")
    output = []
    if len(iteratorStarts) > 0:
        if iteratorStarts[0] != 0:
            output.append(columnString[0:iteratorStarts[0]])
    
    for i, e0 in enumerate(iteratorStarts):
        output.append(columnString[e0:iteratorClose[i]+1])
        if (i < len(iteratorStarts) - 1) and (iteratorClose[i] + 1 < len(columnString) - 1):
            if not (iteratorStarts[i + 1] == iteratorClose[i] + 1):
                output.append(columnString[iteratorClose[i]+1:iteratorStarts[i + 1]])
    if iteratorClose[-1] < len(columnString) - 1:
        output.append(columnString[iteratorClose[-1] + 1:])
    
    return output

def checkValidMath(inputString):
    digits = []
    start = 0
    operations = []
    for i, e in enumerate(inputString):
        if e == "+" or e == "-" or e == "*":
            digits.append(inputString[start:i])
            operations.append(e)
            start = i + 1
    
    if start >= len(inputString):
        print(f"Error in math expression: {inputString}. Likely due to trailing operation.")
        return False
    digits.append(inputString[start:])
    for digit in digits:
        if not (digit.isdigit()):
            print(f"Error in math expression: {inputString}. Likely due to invalid characters. Allowed terms: Positive Integers, +, -, *, &")
            return False
    
    if len(operations) + 1 != len(digits):
        print(f"Error in math expression: {inputString}. Likely due to extra operation")
        return False
    return True

def evaluteSimpleMath(inputString):
    assert(checkValidMath(inputString))
    digits = []
    start = 0
    operations = []
    for i, e in enumerate(inputString):
        if e == "+" or e =="-" or e == "*":
            digits.append(inputString[start:i])
            operations.append(e)
            start = i + 1
    

    digits.append(inputString[start:])
    intDigits = []
    for digit in digits:
        intDigits.append(int(digit))
    count = intDigits[0]
    for i, operation in enumerate(operations):
        if operation == "+":
            count += intDigits[i + 1]
        elif operation == "-":
            count -= intDigits[i + 1]
        else:
            count *= intDigits[i + 1]
    return count
        
    

# checks if a iterator is valid, does not check if the block itself is valid.
def validIterator(iteratorString):
    # pre, iterator string must come from a valid iterator split
    if "$" not in iteratorString: # not an iterator
        return True

    splitIterator = iteratorString.split("[") # this is fine due to iterator split checks
    iteratorData = splitIterator[1][:-1] # also safe due to iterator split checks

    iteratorFunction = splitIterator[0]
    openingFunction = findAllStrings(iteratorFunction, "(")
    closingFunction = findAllStrings(iteratorFunction, ")")
    splitFunction = findAllStrings(iteratorFunction, ",")
    if (len(openingFunction) != 1 or len(closingFunction) != 1 or len(splitFunction) != 1):
        print(f"Iterator Range Error 0: {iteratorFunction}")
        return False

    if not (openingFunction[0] < splitFunction[0] and splitFunction[0] < closingFunction[0]):
        print(f"Iterator Range Error 1: {iteratorFunction}")
        return False
    iteratorFunction = iteratorFunction[2:-1] # now safe
    functionRangeStrings = iteratorFunction.split(",")
    for e in functionRangeStrings:
        if not e.isdigit():
            print(f"Non digit in iterator range: {iteratorFunction}")
            return False
    
    functionRange = [int(e) for e in functionRangeStrings]
    if functionRange[0] < functionRange[1]:
        valueRange = [i for i in range(functionRange[0], functionRange[1] + 1)]
    else:
        valueRange = [i for i in reversed(range(functionRange[1], functionRange[0] + 1))]
    
    # replace then check math
    for i in valueRange:
        newTerm = iteratorData[:]
        replacementPosistions = findAllStrings(newTerm, "&")
        for replacementPos in replacementPosistions:
            newTerm = newTerm[:replacementPos] + str(i) + newTerm[replacementPos + 1:]
        
        openingMath = findAllStrings(newTerm, "(")
        closingMath = findAllStrings(newTerm, ")")
        if len(closingMath) != len(openingMath):
            print("Unbalanced Math brackets in iterator.")
            return False
        
        for i in range(len(closingMath)):
            if not (openingMath[i] < closingMath[i]):
                print("Math brackets error in iterator.")
                return False

        mathPairs = [(openingMath[i], closingMath[i]) for i in range(len(openingMath))]
        
        for pair in mathPairs:
            if not checkValidMath(newTerm[pair[0] + 1:pair[1]]):
                print('math error')
                return False
    return True


# expands the iterator
def expandIterator(iteratorString):
    assert(validIterator(iteratorString))
    if "$" not in iteratorString: # we do not need to modifiy this string
        return iteratorString
    splitIterator = iteratorString.split("[")
    iteratorFunction = splitIterator[0][2:-1]
    iteratorData = splitIterator[1][:-1] # remove ]
    functionRange = [int(e) for e in iteratorFunction.split(",")]
    if functionRange[0] < functionRange[1]:
        valueRange = [i for i in range(functionRange[0], functionRange[1] + 1)]
    else:
        valueRange = [i for i in reversed(range(functionRange[1], functionRange[0] + 1))]
    
    expandedString = ""
    for i in valueRange:
        newTerm = iteratorData[:]
        replacementPosistions = findAllStrings(newTerm, "&")
        for replacementPos in replacementPosistions:
            newTerm = newTerm[:replacementPos] + str(i) + newTerm[replacementPos + 1:]
        
        openingMath = findAllStrings(newTerm, "(")
        closingMath = findAllStrings(newTerm, ")")
        mathPairs = [(openingMath[i], closingMath[i]) for i in range(len(openingMath))]
        
        if len(mathPairs) != 0:
            finalTerm = ""
            start = 0
            for pair in mathPairs:
                finalTerm += newTerm[start:pair[0]]
                finalTerm += str(evaluteSimpleMath(newTerm[pair[0] + 1:pair[1]]))
                start = pair[1] + 1
            finalTerm += newTerm[mathPairs[-1][1] + 1:]

            expandedString += finalTerm
        else:
            expandedString += newTerm
    
    return expandedString


def checkSplitBlocks(expandedColumnString):
    openingBlocks = findAllStrings(expandedColumnString, "{")
    closingBlocks = findAllStrings(expandedColumnString, "}")

    if not (len(closingBlocks) == len(openingBlocks)):
        print("Error Unequal amount of brackets in column.")
        return False
    for i in range(len(openingBlocks)):
        if not (openingBlocks[i] < closingBlocks[i]):
            print("Error Column bracket mismatch.")
            return False
    return True

# splits an expanded column into individual blocks
def splitBlocks(expandedColumnString):
    assert(checkSplitBlocks(expandedColumnString))
    split = expandedColumnString.split("}{")
    split[0] = split[0][1:]
    split[-1] = split[-1][:-1]
    return split
    

# checks if the block is valid
def validBlock(blockString):
    nameSep = findAllStrings(blockString, ":")
    if len(nameSep) > 1:
        print("InvalidBlock1")
        return False
    
    nameLess = ""
    if len(nameSep) == 1:
        nameLess += blockString[nameSep[0] + 1:]
    else:
        nameLess += blockString
    virtualHeightSep = findAllStrings(nameLess, "#")
    if len(virtualHeightSep) > 1:
        print("InvalidBlock2")
        return False
    
    nameHeightLess = ""
    if len(virtualHeightSep) == 1:
        nameHeightLess += nameLess[:virtualHeightSep[0]]
        height = nameLess[virtualHeightSep[0] + 1:]
        if not height.isdigit():
            print("InvalidBlock3")
            return False
    else:
        nameHeightLess += nameLess
    IOsplit = findAllStrings(nameHeightLess, "->")
    if len(IOsplit) != 1:
        print("incorrect seperator for function mapping")
        return False
    return True
        
# uses everything above to check if an entire column is valid
def validColumn(columnString):
    if not (checkIteratorSplit(columnString)):
        print("IteratorSplit error above.")
        return False
    columnSplitByIterator = splitColumnToIterator(columnString)
    for iterator in columnSplitByIterator:
        if not validIterator(iterator):
            print("not valid iterator")
            return False
    expanded = "".join([expandIterator(iterator) for iterator in columnSplitByIterator])
    if not checkSplitBlocks(expanded):

        return False
    blocks = splitBlocks(expanded)
    for block in blocks:
        if not validBlock(block):
            return False
    return True




        
# returns a list of columns each having a list of blocks oafter checking for errors

def process(inputString):
    columns = removeWhitespace(inputString).split(";")
    valid = True
    for i, column in enumerate(columns):
        if not validColumn(column):
            print(f"Column Error in column {i} above.\n")
            valid = False
    
    if not valid:
        print("Unable to generate diagram due to errors above.")
        return

    
    # now a list
    columnsSplitByIterator = [splitColumnToIterator(column) for column in columns]
    
    expandedColumns = []
    for column in columnsSplitByIterator:
        columnString = ""
        for iterator in column:
            columnString += expandIterator(iterator)
        expandedColumns.append(columnString)
    
    blocksInColumns = []
    for column in expandedColumns:
        blocksInColumns.append(splitBlocks(column))
    
    return blocksInColumns



# other helpers

def filterOutString(inputString, characters):
    returnStr = ""
    for e in inputString:
        if e not in characters:
            returnStr += e
    
    return returnStr


def filterDictKeys(inputDict, characters):
    return [filterOutString(e, characters) for e in inputDict]