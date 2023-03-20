# format strings
# 1. remove all whitespace
# 2. split by column
# 3. check validity for each column
# 4. remap any shorthands
# 5. expand iterators
# 6. concatenate and return


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
    if not (len(iteratorOpen) == len(iteratorClose) == len(iteratorStarts)):
        return False
    for e0, e1, e2 in iteratorStarts, iteratorOpen, iteratorClose:
        if not (e0 < e1 and e1 < e2):
            return False
    return True

# splits a column into iterators, by finding dollar signs for start, and ] for ends
def splitIterator(columnString):
    # pre
    assert(checkIteratorSplit(columnString))

    iteratorStarts = findAllStrings(columnString, "$")
    iteratorClose = findAllStrings(columnString, "]")

    output = []
    for i, e0 in enumerate(iteratorStarts):
        output.append(columnString[e0:iteratorClose[i]+1])
        if (i < len(iteratorStarts) - 1) and (iteratorClose[i] + 1 < len(columnString) - 1):
            if not (iteratorStarts[i + 1] == iteratorClose[i] + 1):
                output.append(columnString[iteratorClose[i]+1:iteratorStarts[i + 1]])
    if iteratorClose[-1] < len(columnString) - 1:
        output.append(columnString[iteratorClose[-1] + 1:])
    
    return output

def evaluteSimpleMath(inputString):
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
        assert(digit.isdigit())
        intDigits.append(int(digit))
    assert(len(intDigits) == len(operations) + 1)
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
def validIterator(iteratorBlockString):
    pass

# expands the iterator
def expandIterator(iteratorString):
    pass

# splits an expanded column into individual blocks
def splitBlocks(expandedColumnString):
    pass

# checks if the block is valid
def validBlock(blockString):
    pass

# uses everything above to check if an entire column is valid
def validColumn(columnString):
    pass



        


def process(inputString):
    columns = removeWhitespace(inputString).split(";") 

