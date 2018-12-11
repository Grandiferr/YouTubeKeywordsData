

def getChannel(channelId):
    client.channels().list(
                        part = "snippet, statistics",
                        id = channelId).execute().get('items', [])[0]['snippet']['title'] 
                )
    