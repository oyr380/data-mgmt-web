from django.shortcuts import redirect, render
from django.http import HttpResponse
from yt_data.helper import MongoInstance, generate_random_comments, likes_per_view, s_to_m
import time

instance = MongoInstance()

# Create your views here.
def home(request):

    if request.method == 'POST':
        query = request.POST['search']
        yt_channels = []
       # query = '^'+query
        channels = instance.search_for_channels(query)
        if channels != None:
            for channel in channels:
                yt_channels.append({'name':channel['channel'], "subscriber_count":channel['channel_follower_count']})
            
    else:
        channels = instance.grab_all_channels()
        yt_channels = []
        for channel in channels:
            yt_channels.append({'name':channel['channel'], "subscriber_count":channel['channel_follower_count']})
    context = {
        "yt_channels" : yt_channels
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def channel(request, chname=''):
    
    most_liked = instance.grab_most_liked(chname)
    
    most_viewed = instance.grab_most_viewed(chname)
    if request.method == 'POST':
        query = request.POST['search']
        videos = instance.search_for_videos(chname, query)
        page = None
        channel = instance.grab_one_channel(chname)
        total_pages = None
    else:
        page = request.GET.get('page')
        total_pages = instance.grab_max_pages(chname)
        channel = instance.grab_one_channel(chname)
        if page:
            if int(page) == 1 or 1 > int(page) or total_pages < int(page):
                #videos = ["https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO","https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO","https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO", "https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO","https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO","https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO","https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO","https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO","https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO","https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO"] 
                page = 1
                skip = 50 * (page - 1)
                videos = instance.grab_channel_videos(chname, skip)
            else:
                skip = 50 * (int(page) - 1)
                videos = instance.grab_channel_videos(chname, skip)
            #query based on pagination
        else:
            page = 1
            skip = 50 * (page - 1)
            start = time.time()
            videos = instance.grab_channel_videos(chname, skip)
            end = time.time()
            print(end-start)
            #default query (find().limit(10))
    context = {
        'chname' : chname,
        'videos' : videos,
        'page' : page,
        'total_pages' : total_pages,
        'most_liked' : most_liked,
        'most_viewed' : most_viewed,
        'channel' : channel,
    }
    
    return render(request, 'channel.html', context)

def video(request, _id='', chname=''):
    start = time.time()
    video = instance.grab_one_video(_id, chname)
    end = time.time()
    print(end-start)
    if 'comment_count' in video.keys():
        total_coms = video['comment_count'] 
    else:
        if 'comments' in video.keys():
            total_coms = len(video['comments'])
        else:
            total_coms = 0
    if total_coms > 0:
        comments_to_display = generate_random_comments(video['comments'], total_coms) 
    else:
        comments_to_display = 0
    
    lpv = likes_per_view(video['like_count'],video['view_count'])
    duration = s_to_m(video['duration'])
    context = {
        'video' : video, 
        'id' : _id,
        'comments' : comments_to_display,
        'total_coms' : total_coms,
        'lpv' : lpv,
        'duration': duration,
        }
    return render(request, 'video.html', context)