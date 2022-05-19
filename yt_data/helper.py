import pymongo
import math
from random import randint
import datetime

def generate_random_comments(arr, count) -> list:
    commArr = []
    if count < 20:
        r = count
    else:
        r = 20
    for i in range(0,r):
        comm = arr[randint(0, count-1)]
        if comm in commArr:
            while comm in commArr:
                comm = arr[randint(0, count-1)]
            commArr.append(comm)
        else:
            commArr.append(comm)
    return commArr

def likes_per_view(likes, views) -> int:
    if likes == 0:
        return 0
    return math.ceil(views/likes)

def s_to_m(duration) -> str:
    return str(datetime.timedelta(seconds=duration))

def date_convert(date) -> str:
    return (datetime.datetime(int(date[0:4]),int(date[4:6]),int(date[6:])).date)

class MongoInstance:
    def __init__(self):
        self.connection = pymongo.MongoClient('mongodb+srv://bigdata:cs4243@cluster0.k5iv2.mongodb.net/project-test')
        self.db = self.connection['project-test']
        self.videos = self.db['videos']
        self.channels = self.db['channels']
    
    def grab_all_channels(self):
        channels = self.channels.find().sort('channel_follower_count', -1)
        return channels
    
    def grab_one_channel(self, name):
        channel = self.channels.find_one({"channel":name}, {"thumbnails":1})
        return channel
    
    def search_for_channels(self, regex):
        channels = self.channels.find({"channel":{'$regex':regex, '$options': 'i'}}, {"channel":1,"thumbnails":1, "channel_follower_count":1}).sort('channel_follower_count', -1)
        return channels

    def grab_one_video(self, _id, name):
        video = self.videos.find_one({"channel":name,"id":_id})
        return video

    def search_for_videos(self, chname, regex):
        videos = self.videos.find({"channel":chname,"title":{'$regex':regex, '$options': 'i'}}, {"webpage_url":1, "title":1, "thumbnail":1, "id":1})
        if videos:
            return [[x['webpage_url'], x['title'], x['thumbnail'], x['id']] for x in videos]
        else:  
            return None

        

    def grab_most_viewed(self, name):
        video = self.videos.find({"channel":name}, {"title": 1, "id":1}).sort('view_count', -1).limit(1)
        return video[0]

    def grab_most_liked(self, name):
        video = self.videos.find({"channel":name}, {"title": 1, "id":1}).sort('like_count', -1).limit(1)
        return video[0]
    
    def grab_max_pages(self, name) -> int:
        #Might use self.videos.count_documents() instead
        video_count = self.videos.count_documents({"channel":name}  )
        max_pages = math.ceil(video_count / 50)
        return max_pages

    def grab_channel_videos(self, name, skip):
        videos = self.videos.find({"channel":name}, {"webpage_url":1, "title":1, "thumbnail":1, "id":1}).skip(skip).limit(50)
        return [[x['webpage_url'], x['title'], x['thumbnail'], x['id']] for x in videos]
