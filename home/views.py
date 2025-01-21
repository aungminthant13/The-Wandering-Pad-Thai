from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    content1 = "Welcome! The web app is currently under construction! <br><br><br>"
    content2 = "Meanwhile, listen to this Jazz playlist. <br><br>"
    content3 = '<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/37i9dQZF1DWV7EzJMK2FUI?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
    content = content1 + content2 + content3
    return HttpResponse(content)
