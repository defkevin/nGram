import re, enchant, os

def getAllLinesForYear(directory):
    allLines = []
    print(directory)
    for textFile in os.listdir(directory):
        if textFile.endswith(".txt"):
            bookDirectory = directory +"/"+textFile
            bookLines = readFile(bookDirectory)
            allLines = allLines +bookLines
    return allLines

def readFile(filename):
    bookLines = []
    title = ""
    # store lines into array
    try:
        with open(filename) as file_object:
            for line in file_object:
                if line.strip():
                    # find the title
                    line = line.strip()
                    if line.split()[0] == "Title:":
                        title = " ".join(line.split()[1:]).title()
                    bookLines.append(line.strip())
    except:
        print("The file " + filename + " does not exist")
    bookLines = trimLines(bookLines,title)
    return bookLines

#trims the lines from all lines in a file to just the lines of the book
def trimLines(lines, title):
    lineSkipsFront = 0
    lineSkipsEnd = 0
    for line in lines:
        if line.title() == title:
            lines = lines[lineSkipsFront:]
            break
        lineSkipsFront += 1

    for line in lines:
        firstWord, secondWord = "",""
        if (len(line.split()) > 2):
            firstWord = line.split()[0]
            secondWord = line.split()[1]
        # need to find out a better way to find the end of the book file
        if firstWord == "***" and secondWord == "END":
            # while line.split()
            lines = lines[:lineSkipsEnd - 1]
            break
        lineSkipsEnd += 1
    return lines

def getWords(bookLines):
    allWords = []
    for line in bookLines:
        wordsInOneLine = line.split()
        for word in wordsInOneLine:
            # strip punctuation
            word = re.sub(r'[^\w\s]', '', word)
            # word = re.sub(r"/p{P}(?<!-)","",word) # keep dashes regex option

            #dont include words that are empty
            if(len(word) is not 0):
                allWords.append(word)
    return allWords

def nGram(allWords,n):
    wordDict = {}
    for value in range(0,len(allWords)-(n-1)):
        #makes a n-gram using n words
        word = " ".join(allWords[value:value+n])
        if word not in wordDict:
            wordDict[word] = 1;
        else:
            wordDict[word] = wordDict[word]+1
    # print(str(n)+"Gram: " + str(wordDict))
    return wordDict


def spellChecker(word):
    d = enchant.Dict("en_US")
    if d.check(word) is not True:
        suggestions = d.suggest(word)
        if len(suggestions) is not 0:
            return suggestions[0]
    return word


def returnDictionaries(directory, startYear,endYear):
    print("returnDictionaries: "+directory)
    dictionaries = {}
    for year in range(startYear,endYear+1):
        yearDict = {}
        currDirectory = directory+"/"+str(year)
        allBookLines = getAllLinesForYear(currDirectory)
        for i in range(1,6):
            allBookWords = getWords(allBookLines)
            wordDict = nGram(allBookWords, i)
            yearDict[i] = wordDict
        dictionaries[year] = yearDict
    return dictionaries


def nGramDistributionByYear(dictionaries, nGram):
    n = len(nGram.split(" "))
    distributionsByYear = []
    nGramCount = 0
    totalnGramCount = 0
    for year in dictionaries:
        nGramCount = dictionaries[year][n].get(nGram,0)
        totalnGramCount = sum(dictionaries[year][n].values())
        distribution = (nGramCount*1.0)/totalnGramCount
        distributionsByYear.append(distribution)
    return distributionsByYear



if __name__ == "__main__":
    dictionaries = returnDictionaries("../challenge_Files",2012,2016)
    print(nGramDistributionByYear(dictionaries, "the"))
    print(nGramDistributionByYear(dictionaries, "nothing but"))
    print(nGramDistributionByYear(dictionaries, "and"))
    print(nGramDistributionByYear(dictionaries, "Tarzan"))
    print(nGramDistributionByYear(dictionaries, "to be"))
