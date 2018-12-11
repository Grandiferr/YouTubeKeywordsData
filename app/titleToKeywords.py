
from debug import *
import re

def strToKeyword(kw):
    return str.lower(kw.replace("-", "").replace("&", "").replace("|", ""))

def titleToKeywords_one(title):
    wordList = title.split(" ")

    wordList = [re.sub(r'\W+', '', word) for word in wordList]
    
    wordListLen = len(wordList)
    phraseList = []
    for phraseLen in range(1, 4):
        for index in range(0, (wordListLen - (phraseLen-1))):


            phrase = " ".join(wordList[index:phraseLen + index])
            phraseList.append(phrase)
    return phraseList


def titleToKeywords_all(titleList):
    if DEBUG: print("titleToKeywords_all:    Working on a new title list num of titles: ...", len(titleList))
    phraseList = []
    count = 1
    for title in titleList:
        if DEBUG: print("titleToKeywords_all:  %i / %i titles..." % (count, len(titleList) ))
        count += 1
        phraseList = phraseList + titleToKeywords_one(title)
    return phraseList


def insertTitle_one(title):
    phraseList = titleToKeywords_one(title)
    return ", ".join(phraseList)


def insertTitle_all(titleList):
    return titleToKeywords_all(titleList)
    

