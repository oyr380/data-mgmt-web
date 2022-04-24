from django.shortcuts import redirect, render
from django.http import HttpResponse
from yt_data.helper import MongoInstance

instance = MongoInstance()

# Create your views here.
def home(request):
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
    page = request.GET.get('page')
    total_pages = instance.grab_max_pages(chname)
    most_liked = instance.grab_most_liked(chname)
    most_viewed = instance.grab_most_viewed(chname)
    channel = instance.grab_one_channel(chname)
    #if request.method == 'POST':
     #   return redirect(request.path+'?page=2')
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
        videos = instance.grab_channel_videos(chname, skip)
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