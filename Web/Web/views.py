from utils.Search import UpSearch, VideoSearch
from utils import DataProcessor
from django.http.response import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from datetime import datetime
import os, random, json

# Create your views here.


def root(req):
    return redirect('videoList/')


def video(req, id):
    try:
        id = int(id)
    except:
        return HttpResponseNotFound()
    props = VideoSearch(2, -1, id)
    if props == {}:
        return HttpResponseNotFound()
    return render(req, "Video.html", props)


def videoList(req):
    page = req.GET.get('page', '1')
    try:
        page = int(page)
    except:
        return HttpResponseNotFound()
    props = VideoSearch(0, page)
    return render(req, 'VideoList.html', props)

def upList(req):
    page = req.GET.get('page', '1')
    try:
        page = int(page)
    except:
        return HttpResponseNotFound()
    props = UpSearch(0, page)
    return render(req, 'upList.html', props)
        
def up(req, id):
    page = req.GET.get('page', '1')
    try:
        id = int(id)
        page = int(page)
    except:
        return HttpResponseNotFound()
    props = UpSearch(2, page, id)
    if props == {}:
        return HttpResponseNotFound()
    return render(req, 'Up.html', props)

def search(req):
    page = req.GET.get('page', '1')
    try:
        page = int(page)
    except:
        return HttpResponseNotFound()
    type = req.GET.get('type')
    keyword = req.GET.get('keyword')
    
    if type == 'video':
        props = VideoSearch(1, page, keyword)
        return render(req, 'VideoList.html', props)
    elif type == 'up':
        props = UpSearch(1, page, keyword)
        return render(req, 'UpList.html', props)
    else:
        return render(req, "404.html")
    

def mergeData(req):
    return DataProcessor.MergeData()
