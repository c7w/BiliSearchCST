from django.http.response import HttpResponse
from Web.models import Comment, Tag, Up, Video
import os
import json
import time
import datetime


def MergeData():
    authorCount = 0
    videoCount = 0
    
    
    # process authors
    upl = os.listdir('./ResultPool/UpResult')
    upr = []
    for fileName in upl:
        f = open('./ResultPool/UpResult/' + fileName, 'r', encoding='utf-8')
        j = json.load(f)
        f.close()
        
        author = Up(id=j['id'],
                    username=j["username"],
                    signature=j['signature'],
                    level=j['level'],
                    avatarUrl=j['avatarUrl'],
                    followerCount=j['followerCount'],
                    followingCount=j['followingCount'])
        upr.append(author)
        authorCount += 1
        os.remove('./ResultPool/UpResult/' + fileName)
    Up.objects.bulk_create(upr)

    # process videos
    vil = os.listdir('./ResultPool/CrawlResult')
    vir = []
    cmr = []
    tgr = []
    for fileName in vil:
        f = open('./ResultPool/CrawlResult/' + fileName, 'r', encoding='utf-8')
        j = json.load(f)
        f.close()
        video = Video(id=j['id'],
                    title=j['title'],
                    abstract=j['abstract'],
                    uploadTime=datetime.datetime.fromtimestamp(
                        j['uploadTime']),
                    playCount=j['playCount'],
                    commentCount=j['commentCount'],
                    bulletCommentCount=j['bulletCommentCount'],
                    imageUrl=j['imageUrl'],
                    like=j['feedback']['like'],
                    coin=j['feedback']['coin'],
                    star=j['feedback']['star'],
                    share=j['feedback']['share'],
                    author=Up.objects.get(id=j['authorId'])
                    )
        vir.append(video)
        for comment in j['comments']:
            cm = Comment(video=video, content=comment)
            cmr.append(cm)
        for tag in j['tags']:
            tg = Tag(video=video, tagName=tag)
            tgr.append(tg)
        videoCount += 1
        os.remove('./ResultPool/CrawlResult/' + fileName)
    Video.objects.bulk_create(vir)
    Comment.objects.bulk_create(cmr)
    Tag.objects.bulk_create(tgr)
    return HttpResponse(f'Data process finished with {authorCount} authors and {videoCount} videos imported.')
