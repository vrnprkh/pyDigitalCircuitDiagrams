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

def splitIteratorTest():


def runAllStringProcessorTests():
    removeWhiteSpaceTest()
    findAllStringsTest()
    print("Passed All String Processor Tests!")

if __name__ == "__main__":
    runAllStringProcessorTests()
