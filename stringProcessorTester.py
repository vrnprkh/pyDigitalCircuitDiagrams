from stringProcessor import *

def removeWhiteSpaceTest():
    assert(removeWhitespace("hello \n testing ending \n") == "hellotestingending")

def findAllStringsTest():
    testString1 = "012345 $ 1 $ $ $"
    testString2 = ""
    testString3 = "$ $"
    assert(findAllStrings(testString1, "$") == [7,11,13,15])
    assert(findAllStrings(testString1, "$ $") == [11, 13])
    assert(findAllStrings(testString1, "") == [i for i in range(len(testString1) + 1)])
    assert(findAllStrings(testString2, " ") == [])
    assert(findAllStrings(testString3, "Long text") == [])


def checkIteratorSplitTest():
    testBlock = "$(0,3)[{XOR:a(&),b(&)->fg(&)}{AND:a(&),b(&)->fcout(&)}]{IteratorFreeBlock:a,b->c}$(0,2)[{a,b->c(&)}]$(3,4)[{a,b->c}]"
    assert(checkIteratorSplit(testBlock))
    testBlock2 = "$[][[]]"
    assert(not checkIteratorSplit(testBlock2))

def splitIteratorTest():
    testBlock = "$(0,3)[{XOR:a(&),b(&)->fg(&)}{AND:a(&),b(&)->fcout(&)}]{IteratorFreeBlock:a,b->c}$(0,2)[{a,b->c(&)}]$(3,4)[{a,b->c}]{ClosedBlocks}{}"
    expectedSplit = [
        "$(0,3)[{XOR:a(&),b(&)->fg(&)}{AND:a(&),b(&)->fcout(&)}]",
        "{IteratorFreeBlock:a,b->c}",
        "$(0,2)[{a,b->c(&)}]",
        "$(3,4)[{a,b->c}]",
        "{ClosedBlocks}{}",
    ]

    assert(splitIterator(testBlock) == expectedSplit)

# note order of operations is left to right
def evaluteSimpleMathTest():
    expr1 = "5*4+3-2+1*6"
    expr2 = "10+3*3-20*2"
    expr3 = "3*3*3-0+0-3"
    assert(evaluteSimpleMath(expr1) == 132)
    assert(evaluteSimpleMath(expr2) == 38)
    assert(evaluteSimpleMath(expr3) == 24)


def runAllStringProcessorTests():
    removeWhiteSpaceTest()
    findAllStringsTest()
    checkIteratorSplitTest()
    splitIteratorTest()
    evaluteSimpleMathTest()
    print("Passed All String Processor Tests!")

if __name__ == "__main__":
    runAllStringProcessorTests()
