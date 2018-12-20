import httplib2
import os
import sys
from pymongo import MongoClient
from googleapiclient.discovery import build
from debug import *
#CLIENT_SECRETS_FILE = r"C:\Users\Oliver\Desktop\Misc Code\python\KC\env\Lib\site-packages\google\google-api-python-client-1.7.5\tests\data\client_secrets.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
DEVELOPER_KEY = ""

#last 30 days of youtube videos titles from every channel in the database
#get list of youtube videos

def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs

#returns list of video IDs given search criteria
def youtube_search_videos(client, **args):
    args = remove_empty_kwargs(**args)
    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = client.search().list(
        **args
    ).execute()
    videos = []
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result["id"]["videoId"])
    return videos

#take yt videoId string list
#return list of dictionary containing video stats
def youtube_video_stats(client, videoIdList):
    vidList = client.videos().list(
        part = "snippet,statistics",
        id = ",".join(videoIdList)
    ).execute()
    
    return vidList.get('items', [])
    

#UClficNojymRrJdbdjsE7jgQ
