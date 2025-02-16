from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    content1 = "<br><h2>Welcome! The web app is currently under construction!</h2> <br><br><br>"
    content2 = "Meanwhile, listen to this Jazz playlist. <br><br>"
    content3 = '<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/37i9dQZF1DWV7EzJMK2FUI?utm_source=generator" width="70%" height="500" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
    content = "<center>" + content1 + content2 + content3 + "</center>"
    return HttpResponse(content)
