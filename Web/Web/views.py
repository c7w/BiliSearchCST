from utils import DataProcessor
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from datetime import datetime
import os, random, json

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
        "comments": ["阿奴if的哈UI的哈虽短是你的哦阿斯顿你把苏大哥i", "ajshdiuasdoashdoasod"],
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
    dir = list(os.listdir("../Crawler/Result/CrawlResult"))
    random.shuffle(dir)
    videos = []
    for i in dir[0:10]:
        f = open("../Crawler/Result/CrawlResult/" + i, 'r', encoding='utf-8')
        j = json.load(f)
        g = open("../Crawler/Result/UpResult/" +
                 str(j['authorId']) + '.json', 'r', encoding='utf-8')
        j['author'] = json.load(g)
        j['star'] = j['feedback']['star']
        if (len(j['abstract']) > 75):
            j['shortAbstract'] = j['abstract'][0:75] + "..."
        else:
            j['shortAbstract'] = j['abstract']
        j['uploadTime'] = datetime.fromtimestamp(
            j['uploadTime']).strftime('%Y-%m-%d %H:%M:%S')
        videos.append(j)
        f.close()
        g.close()
    props = {"videos": videos, "page": {"title": "123"}}
    return render(req, 'VideoList.html', props)

def upList(req):
    dir = list(os.listdir("../Crawler/Result/UpResult"))
    random.shuffle(dir)
    authors = []
    for i in dir[0:10]:
        g = open("../Crawler/Result/UpResult/" + i, 'r', encoding='utf-8')
        j = json.load(g)
        authors.append(j)
    props = {"authors": authors, "page": {"title": "我是标题"}}
    return render(req, 'upList.html', props)
        
def up(req, id):
    videos = [{
        "id": 1005684,
        "title": "【古剑奇谭二】- 共我迢迢 - 宣传视频",
        "abstract": "自制DLC - 共我迢迢 - 宣传视频。剪辑by奢另 高清下载 http://vdisk.weibo.com/s/drHxhkV67Pjn",
        "authorId": 697350,
        "uploadTime": 1394551345.0,
        "playCount": 32563,
        "commentCount": 55,
        "bulletCommentCount": 678,
        "imageUrl": "http://i1.hdslb.com/bfs/archive/127d3d9f03f682dead2554411046342adc494855.jpg",
        "feedback": {
            "like": "35",
            "coin": "414",
            "star": "644",
            "share": "44"
        },
        "comments": [
            "“这茫茫浮世，终于有人和我心意相通“…………这话一出来我的眼泪就…………TAT！！",
            "共我迢迢的宣动视频。古剑二游戏的自制DLC，建议百度搜索。但是不要去看《太好的梦别信》。但是不要去看《太好的梦别信》。但是不要去看《太好的梦别信》。嗯，重要的事要说三遍。被虐到，不怪我。",
            "喜欢阿夜好幸福！给技术喵表白！",
            "收集萌新",
            "我爱你啊大祭司！"
        ],
        "tags": [
            "游戏集锦",
            "游戏",
            "单机游戏",
            "古剑奇谭",
            "古剑奇谭二",
            "初七",
            "沈夜",
            "古剑奇谭2",
            "自制DLC",
            "流月城黑偃术",
            "技术娘屌炸天",
            "共我迢迢"
        ]
    }, {
        "id": 1005727,
        "title": "各种闪现杀教学 lol英雄联盟",
        "abstract": "优酷 搬运",
        "authorId": 381738,
        "uploadTime": 1394553436.0,
        "playCount": 12269,
        "commentCount": 3,
        "bulletCommentCount": 41,
        "imageUrl": "http://i0.hdslb.com/bfs/archive/3635f21104b773a97facfc02b961830f42895fc1.jpg",
        "feedback": {
            "like": "0",
            "coin": "0",
            "star": "61",
            "share": "5"
        },
        "comments": [
            "只会嘲讽闪现和以前的勾闪现 现在勾闪现没了简直不幸福",
            "慎的嘲讽闪现始终学不会。。。经常按了闪现也只能闪到原来的落点",
            "收集萌新"
        ],
        "tags": [
            "英雄联盟",
            "游戏",
            "电子竞技",
            "电子竞技",
            "233",
            "UP主就是妹子",
            "闪现",
            "UP摸摸头",
            "没有TAG的悲剧",
            "UP主忘记锁TAG被调戏系列"
        ]
    }, {
        "id": 1005727,
        "title": "各种闪现杀教学 lol英雄联盟",
        "abstract": "优酷 搬运",
        "authorId": 381738,
        "uploadTime": 1394553436.0,
        "playCount": 12269,
        "commentCount": 3,
        "bulletCommentCount": 41,
        "imageUrl": "http://i0.hdslb.com/bfs/archive/3635f21104b773a97facfc02b961830f42895fc1.jpg",
        "feedback": {
            "like": "0",
            "coin": "0",
            "star": "61",
            "share": "5"
        },
        "comments": [
            "只会嘲讽闪现和以前的勾闪现 现在勾闪现没了简直不幸福",
            "慎的嘲讽闪现始终学不会。。。经常按了闪现也只能闪到原来的落点",
            "收集萌新"
        ],
        "tags": [
            "英雄联盟",
            "游戏",
            "电子竞技",
            "电子竞技",
            "233",
            "UP主就是妹子",
            "闪现",
            "UP摸摸头",
            "没有TAG的悲剧",
            "UP主忘记锁TAG被调戏系列"
        ]
    }, {
        "id": 1005727,
        "title": "各种闪现杀教学 lol英雄联盟",
        "abstract": "优酷 搬运",
        "authorId": 381738,
        "uploadTime": 1394553436.0,
        "playCount": 12269,
        "commentCount": 3,
        "bulletCommentCount": 41,
        "imageUrl": "http://i0.hdslb.com/bfs/archive/3635f21104b773a97facfc02b961830f42895fc1.jpg",
        "feedback": {
            "like": "0",
            "coin": "0",
            "star": "61",
            "share": "5"
        },
        "comments": [
            "只会嘲讽闪现和以前的勾闪现 现在勾闪现没了简直不幸福",
            "慎的嘲讽闪现始终学不会。。。经常按了闪现也只能闪到原来的落点",
            "收集萌新"
        ],
        "tags": [
            "英雄联盟",
            "游戏",
            "电子竞技",
            "电子竞技",
            "233",
            "UP主就是妹子",
            "闪现",
            "UP摸摸头",
            "没有TAG的悲剧",
            "UP主忘记锁TAG被调戏系列"
        ]
    }, {
        "id": 1005727,
        "title": "各种闪现杀教学 lol英雄联盟",
        "abstract": "优酷 搬运",
        "authorId": 381738,
        "uploadTime": 1394553436.0,
        "playCount": 12269,
        "commentCount": 3,
        "bulletCommentCount": 41,
        "imageUrl": "http://i0.hdslb.com/bfs/archive/3635f21104b773a97facfc02b961830f42895fc1.jpg",
        "feedback": {
            "like": "0",
            "coin": "0",
            "star": "61",
            "share": "5"
        },
        "comments": [
            "只会嘲讽闪现和以前的勾闪现 现在勾闪现没了简直不幸福",
            "慎的嘲讽闪现始终学不会。。。经常按了闪现也只能闪到原来的落点",
            "收集萌新"
        ],
        "tags": [
            "英雄联盟",
            "游戏",
            "电子竞技",
            "电子竞技",
            "233",
            "UP主就是妹子",
            "闪现",
            "UP摸摸头",
            "没有TAG的悲剧",
            "UP主忘记锁TAG被调戏系列"
        ]
    }, {
        "id": 1005727,
        "title": "各种闪现杀教学 lol英雄联盟",
        "abstract": "优酷 搬运",
        "authorId": 381738,
        "uploadTime": 1394553436.0,
        "playCount": 12269,
        "commentCount": 3,
        "bulletCommentCount": 41,
        "imageUrl": "http://i0.hdslb.com/bfs/archive/3635f21104b773a97facfc02b961830f42895fc1.jpg",
        "feedback": {
            "like": "0",
            "coin": "0",
            "star": "61",
            "share": "5"
        },
        "comments": [
            "只会嘲讽闪现和以前的勾闪现 现在勾闪现没了简直不幸福",
            "慎的嘲讽闪现始终学不会。。。经常按了闪现也只能闪到原来的落点",
            "收集萌新"
        ],
        "tags": [
            "英雄联盟",
            "游戏",
            "电子竞技",
            "电子竞技",
            "233",
            "UP主就是妹子",
            "闪现",
            "UP摸摸头",
            "没有TAG的悲剧",
            "UP主忘记锁TAG被调戏系列"
        ]}]
    props = {"up": {
        "id": 245869,
        "username": "尚在天国EX",
        "signature": "I will be prepared next time.... 商务vx：fengbizhetongren ",
        "level": 6,
        "avatarUrl": "https://i1.hdslb.com/bfs/face/ab4a110cd994c3a3e152410fa8dcbb0a5f074aab.jpg",
        "followerCount": "31.6万",
        "followingCount": "212"
    }, "videos": videos,
        "pagination": {"current": 1, "max": 10, "list": ['L', 1, 2, 3, 4, 5, -1, 9, 10, 'R'],
                       "baseUrl": '/up/18008?'}
    }
    return render(req, 'Up.html', props)

def search(req):
    # TODO
    return render(req, "404.html")
    pass

def mergeData(req):
    return DataProcessor.MergeData()