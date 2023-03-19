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


# splits a column into iterators.
def splitIterator(columnString):
    iteratorStarts = findAllStrings(columnString, "$")



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
    formatString = removeWhitespace(inputString)
    columns = formatString.split(";")
