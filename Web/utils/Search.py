import time
from django.db.models.query_utils import Q
from Web.models import Up, Video, Comment
from utils.Pagination import Pagination

# mode == 0 -> videoList
# mode == 1 -> keyword search
# mode == 2 -> search by id
def VideoSearch(mode, page, *args):
    if mode == 2:
        props = {}
        q = Video.objects.filter(id=args[0])
        if len(q) == 1:
            v = q[0]
            v2 = v.__dict__
            # Datetime
            v2['uploadTime'] = v2['uploadTime'].strftime('%Y-%m-%d %H:%M:%S')
            v2['comments'] = [comment.content for comment in Comment.objects.filter(video_id=v.id)]
            props['video'] = v2
            props['up'] = v.author.__dict__
            return props
        else:
            return {}
        
    else:
        src = []
        if mode == 0:
            q = Video.objects.filter()
            paginator = Pagination(src, "/videoList?")
        elif mode == 1:
            q = Video.objects.filter(
                Q(title__contains=args[0]) | Q(abstract__contains=args[0]))
            paginator = Pagination(src, "/search?type=video&keyword="+args[0])
        else:
            return
        START_TIME = time.time()

        for video in q:
            src.append(video)        
        
        raw_videos = paginator.getPageSrc(page)
        videos = []
        for v in raw_videos:
            v2 = v.__dict__
            # Generate Short Abstract
            if (len(v2['abstract']) > 75):
                v2['shortAbstract'] = v2['abstract'][0:75] + "..."
            else:
                v2['shortAbstract'] = v2['abstract']
            # Datetime
            v2['uploadTime'] = v2['uploadTime'].strftime('%Y-%m-%d %H:%M:%S')
            v2['author'] = v.author.__dict__
            videos.append(v2)
            
        END_TIME = time.time()
        
        props = {"videos": videos,
                "pagination": paginator.getPage(page)}
        if mode == 1:
            props['page'] = {}
            props['page']['title'] = f"搜索完成，共计 {len(src)} 条搜索结果，用时 {round(END_TIME-START_TIME, 4)} 秒."
        return props


def UpSearch(mode, page, *args):
    if mode == 2:
        props = {}
        q = Up.objects.filter(id=args[0])
        if len(q) == 1:
            u = q[0]
            u2 = u.__dict__
            if u2['signature'] == "":
                u2['signature'] = "该用户还没有介绍哦~"
            props['up'] = u2
            # videos
            qvideos = Video.objects.filter(author_id = u.id)
            paginator = Pagination(qvideos, f'/up/{str(args[0])}?')
            props['videos'] = paginator.getPageSrc(page)
            props['pagination'] = paginator.getPage(page)
            return props
        else:
            return {}
    else:
        src = []
        if mode == 0:
            q = Up.objects.filter()
            paginator = Pagination(src, "/upList?")
        elif mode == 1:
            q = Up.objects.filter(
                Q(username__contains=args[0]) | Q(signature__contains=args[0]))
            paginator = Pagination(src, "/search?type=up&keyword="+args[0])
        else:
            return
        
        START_TIME = time.time()

        for up in q:
            src.append(up)

        ups = paginator.getPageSrc(page)
        END_TIME = time.time()

        props = {"authors": ups,
                 "pagination": paginator.getPage(page)}
        if mode == 1:
            props['page'] = {}
            props['page']['title'] = f"搜索完成，共计 {len(src)} 条搜索结果，用时 {round(END_TIME-START_TIME, 4)} 秒."
        return props
