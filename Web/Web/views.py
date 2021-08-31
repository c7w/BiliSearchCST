from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from datetime import datetime

# Create your views here.


def root(req):
    return redirect('videoList/')


def video(req, id):
    # search for ID and return props
    # if not found return 404
    props = {"video": {
        "id": 1005603,
        "title": "各种渣翻唱",
        "abstract": "自制 渣到不能更渣渣",
        "authorId": 3606076,
        "uploadTime": 1394547623.0,
        "playCount": 430,
        "commentCount": 0,
        "bulletCommentCount": 15,
        "imageUrl": "http://i2.hdslb.com/bfs/archive/58e1d15517bcee9c110be00d62e697481fb9ab77.jpg",
        "like": "0",
        "coin": "0",
        "star": "1",
        "share": "3",
        "comments": [],
        "tags": [
            "音乐",
            "翻唱",
            "渣翻唱"
        ]
    }, "up": {
        "id": 18008,
        "username": "大门内庭",
        "signature": "Hack & Mod !",
        "level": 6,
        "avatarUrl": "https://i2.hdslb.com/bfs/face/ff3e626e4c9fd52457203da032b2859fa3fe3f34.jpg",
        "followerCount": "2620",
        "followingCount": "59"
    }}
    props['video']['uploadTime'] = datetime.fromtimestamp(
        props['video']['uploadTime']).strftime('%Y-%m-%d %H:%M:%S')
    return render(req, "Video.html", props)

def videoList(req):
    props = {}
    return render(req, 'VideoList.html', props)

def up(req, id):
    props = {}
    return render(req, 'Up.html', props)