import pymongo
import math

class MongoInstance:
    def __init__(self):
        self.connection = pymongo.MongoClient('mongodb+srv://bigdata:cs4243@cluster0.k5iv2.mongodb.net/test')
        self.db = self.connection['project-test']
        self.videos = self.db['videos']
        self.channels = self.db['channels']
    
    def grab_all_channels(self):
        channels = self.channels.find().sort('channel_follower_count', -1)
        return channels
    
    def grab_one_channel(self, name):
        channel = self.channels.find_one({"channel":name})
        return channel

    def grab_most_viewed(self, name):
        video = self.videos.find({"channel":name}).sort('view_count', -1).limit(1)
        return video[0]

    def grab_most_liked(self, name):
        video = self.videos.find({"channel":name}).sort('like_count', -1).limit(1)
        return video[0]
    
    def grab_max_pages(self, name) -> int:
        #Might use self.videos.count_documents() instead
        video_count = len(list(self.videos.find({"channel":name}, {"webpage_url":1})))
        max_pages = math.ceil(video_count / 50)
        return max_pages

    def grab_channel_videos(self, name, skip):
        #Query is set like this so it only returns webpage_url rather than all fields (saves a bunch of time). This will be changed to return most relevant data to be display
        #On channel page (Such as title, date maybe?)
        videos = self.videos.find({"channel":name}, {"webpage_url":1, "title":1, "thumbnail":1, "id":1}).skip(skip).limit(50)
        return [[x['webpage_url'], x['title'], x['thumbnail'], x['id']] for x in videos]