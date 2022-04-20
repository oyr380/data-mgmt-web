from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    yt_channels = [{'name': "Eminem", "subscriber_count" : 51000000 }, {"name" : "Pewdiepie", "subscriber_count" : 111000000}]
    context = {
        "yt_channels" : yt_channels
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def channel(request, chname=''):
    videos = ["https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO","https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO","https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO", "https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO","https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO","https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO","https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO","https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO","https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO","https://www.youtube.com/watch?v=X-TkrWpO75k&ab_channel=EminemVEVO"]
    context = {
        'chname' : chname,
        'videos' : videos
    }
    return render(request, 'channel.html', context)