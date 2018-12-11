from ytScrapeToDBFunctions import *
import db
from titleToKeywords import *
from models import Channel
from dbInsertKeywords import *
from googleapiclient.discovery import build
from datetime import *
from debug import *

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
DEVELOPER_KEY = "AIzaSyA9Ka0KQ5xSNfVKISUaBRRpy7FrOxooFp0"
channelIds = []

client = build(API_SERVICE_NAME, API_VERSION, developerKey=DEVELOPER_KEY)

#take yt client, channelId, maxResults, startdate, order
def getVideosFromChannel(channelId, tags = [], maxResults = 20,order = "date", sinceNDays = 7, beforeNDays = 0 ):
        if DEBUG: print(
                "getVideosFromChannel:  Searching for videos from channel ...", 
                client.channels().list(
                        part = "snippet",
                        id = channelId).execute().get('items', [])[0]['snippet']['title'] 
                )
        
        videoIds = youtube_search_videos(client, part= "snippet", tags = tags, channelId = channelId, maxResults = maxResults, order = order, publishedAfter= (datetime.now() - timedelta(days = sinceNDays)).isoformat('T') + "Z", publishedBefore= (datetime.now() - timedelta(days = beforeNDays)).isoformat('T') + "Z")
        return youtube_video_stats(client, videoIds)


def getVideosFromAllChannels(tags = [], maxResults = 20,order = "date", sinceNDays = 7, beforeNDays = 0):
        videos = []
        for channel in Channel.objects():
                videos = videos + getVideosFromChannel(channel.ytUserID, tags,maxResults, order, sinceNDays, beforeNDays)
        return videos


