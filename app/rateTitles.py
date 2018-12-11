from titleToKeywords import *
from models import Keyword
from dbInsertKeywords import *
import operator
from getVideos import *
from debug import *
from matplotlib.pyplot import plot, show, axis
from titleToKeywords import strToKeyword



def rateTitle(title):
    kws = titleToKeywords_one(title)
    keywords = []
    for kw in kws:
        KeywordObject = Keyword.objects(key = strToKeyword(kw))
        if KeywordObject: keywords.append(KeywordObject[0])
    rating = 0
    for kw in keywords:
        if (kw.volume > 10000):
            rating += (kw.cpc / kw.volume)
    return rating

#takes a list of yt videos, and returns a dictionary {title:rating}
def rateTitles(videoList):
    if DEBUG: print("rateTitles:    Rating a list of video titles...")
    titleList = [i['snippet']['title'] for i in videoList]
    ratingDict = {}
    unknownKeywords = []
    keywords = []
    if DEBUG: print("rateTitles:    Sending a title list to titleToKeywords_all...")
    kws = titleToKeywords_all(titleList)
    for kw in kws:
        KeywordObject = Keyword.objects(key = strToKeyword(kw))
        if (not KeywordObject):

            unknownKeywords.append(kw)
    if DEBUG: print("rateTitles:    Sending %i unknown keywords to dbInsertKeywords for no return..." % len(unknownKeywords))
    dbInsertKeywords(unknownKeywords, False)
    for title in titleList:
        ratingDict[title] = rateTitle(title)
    if DEBUG: print("rateTitles:    Returning a rating dictionary...")
    return ratingDict


def titlesRateViewCount():
    videos = [i for i in getVideosFromChannel(channelId = "UCvxzTKmHYIvGJMHXCkOQSoA",order = "date", sinceNDays= 90, beforeNDays= 30, maxResults=50)]
    ratingDict = rateTitles(videos)
    videos = [ [i['snippet']['title'], ratingDict[i['snippet']['title']]*100000, int(([i['statistics']['viewCount']])[0])] for i in videos]
    sortedList = sorted(videos, key = lambda video: video[2])
    for p in sortedList:
        print(p)

    x = [i[2] for i in videos]
    y = [i[1] for i in videos]
    plot(x, y, 'ro')
    axis([0,3e7, 0, 20])
    show()
    import numpy
    print(numpy.corrcoef(x, y)[0, 1])

    return videos

titlesRateViewCount()





