from models import Channel
from bs4 import BeautifulSoup
from pandas import DataFrame
import requests
import re
import datetime
from ytScrapeToDBFunctions import *
from debug import *


SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
DEVELOPER_KEY = "AIzaSyA9Ka0KQ5xSNfVKISUaBRRpy7FrOxooFp0"

#INSERTS CHANNEL INFORMATION INTO KC DATABASE
# #NOTE: YOUTUBE HAS 2 DIFFERENT ID TYPES, USER AND CHANNEL
# SOCIAL BLADE CAN USE THEM INTERCHANGABLY FOR URL, WITH YT USER/CHANNEL MUST BE DISTINGUISHED
ytUserID_ = "UCkvWlsTswUtMVrEzlu-1sVg"
channel = Channel()
def insertChannel(ytUserID_, tags_, comment_):
    ytUserID_ = ytUserID_

    #attempt to change username to channel ID
    client = build(API_SERVICE_NAME, API_VERSION, developerKey=DEVELOPER_KEY)
       
    results = client.channels().list(
        part = "snippet,contentDetails,statistics",
        forUsername = ytUserID_
    ).execute()
    responseList = results.get('items', [])
    if len(responseList) > 0: 
        ytUserID_ = responseList[0]['id']
    try:
        URL = "https://socialblade.com/youtube/channel/" + ytUserID_
        req = requests.get(URL)
        soup = BeautifulSoup(req.text, 'html.parser')
        ##SCRAPE
        ytURL_ = soup.find_all('a', href=True)[121]['href']
        subscriberCount_= soup.find(id="youtube-stats-header-subs").contents[0]
        country_ = soup.find(id="youtube-stats-header-country").contents[0]
        sd = soup.find_all(style = "font-weight: bold;")[5].contents[0]
        sd = sd.replace("st","")
        sd = sd.replace("nd","")
        sd = sd.replace("rd","")
        sd = sd.replace("th","")
        startdate_ = datetime.datetime.strptime(sd, "%b %d, %Y")
        earnings_= soup.find(style = "font-size: 1.4em; color:#41a200; font-weight: 600; padding-top: 20px;").contents[0]
        eList = earnings_.split("$")
        eList[1] = eList[1].replace(" - ", "")
        eList = eList[1:3]
        for t in range(len(eList)) : 
            if eList[t].find("K") != -1:
                eList[t] = 1000*float(eList[t].replace("K", ""))
            elif eList[t].find("M") != -1:
                eList[t] = 1000000*float(eList[t].replace("M", ""))
        minMonthEarnings_ = int(float(eList[0]))
        maxMonthEarnings_ = int(float(eList[1]))
        subscriberRank_ = soup.find(style="font-size: 1.6em; color:#41a200; padding-top: 10px; font-weight: 600;").contents[0].replace(",", "")
        subscriberRank_ = int(subscriberRank_[0:len(subscriberRank_)-2])
        viewRank_ = soup.find(id="afd-header-videoview-rank").contents[0].replace(",", "")
        viewRank_ = int(viewRank_[0:len(viewRank_)-2])
        title_ = soup.find(style="float: left; font-size: 1.4em; font-weight: bold; color:#333; margin: 0px; padding: 0px; margin-right: 5px;").contents[0]
        ##IF CHANNEL ALREADY IN DATABASE UPDATE IT, OTHERWISE INSERT IT
        if (Channel.objects(ytUserID = ytUserID_) or Channel.objects(URL = ytURL_)):
            channel = Channel.objects(ytUserID = ytUserID_)
            channel.update_one(set__title = title_)
            channel.update_one(set__URL = ytURL_)
            channel.update_one(set__socialblade = URL)
            channel.update_one(set__minMonthEarnings = minMonthEarnings_)
            channel.update_one(set__maxMonthEarnings = maxMonthEarnings_)
            channel.update_one(set__subscriberCount = subscriberCount_)
            channel.update_one(set__subscriberRank = subscriberRank_)
            channel.update_one(set__viewRank = viewRank_)
            channel.update_one(push_all__tags=tags_)
            if (comment_ != ""): channel.update_one(push__comments = comment_)
        else:
            # print(title_)
            # print(startdate_)
            # print(subscriberCount_)
            # print(country_ )
            # print(URL)
            # print(ytURL_)
            # print(minMonthEarnings_)
            # print(maxMonthEarnings_)
            # print(subscriberRank_)
            # print(viewRank_)
            # init Channel object
            channel = Channel(
                title = title_,
                ytUserID = ytUserID_,
                startdate = startdate_,
                country = country_,
                URL = ytURL_,
                tags = tags_,
                comments = [comment_],
                socialblade = URL,
                minMonthEarnings = minMonthEarnings_,
                maxMonthEarnings = maxMonthEarnings_,
                subscriberRank = subscriberRank_,
                subscriberCount = subscriberCount_,
                viewRank = viewRank_
            )
            channel.save()
            print("entry updated/made")
    except (AttributeError, IndexError) as e:
        print("INVALID TARGET CHANNEL ID: " + ytUserID_)
        pass



def main():
    ex = False
    while( not ex):
        ID = input("Enter User ID or 'exit'\n")
        if ID == "exit":
            ex = True
        else:
            tag = input('Enter Tags:\n').split(", ")
            comment = input('Enter Comment:\n')
            insertChannel(ID, tag, comment)
main()
#UClficNojymRrJdbdjsE7jgQ