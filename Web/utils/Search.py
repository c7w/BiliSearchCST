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
            v2['comments'] = [
                comment.content for comment in Comment.objects.filter(video_id=v.id)]
            props['video'] = v2
            props['up'] = v.author.__dict__
            props['page'] = {}
            props['page']['head'] = "视频详情"
            return props
        else:
            return {}

    else:
        START_TIME = time.time()
        if mode == 0:
            q = Video.objects.all()
            paginator = Pagination(q, "/videoList?", length=q.count())
        elif mode == 1:
            q = Video.objects.filter(
                Q(title__contains=args[0]) | Q(abstract__contains=args[0]))
            paginator = Pagination(
                q, "/search?type=video&keyword="+args[0], length=q.count())
        else:
            return

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
        props['page'] = {}
        if mode == 1:
            props['page']['head'] = "视频搜索"
            if props['pagination'] != {}:
                props['page'][
                    'title'] = f"搜索完成，共计 {props['pagination']['count']} 条搜索结果，用时 {round(END_TIME-START_TIME, 6)} 秒."
            else:
                props['page'][
                    'title'] = f"搜索完成，无搜索结果，用时 {round(END_TIME-START_TIME, 6)} 秒."
        else:
            props['page']['head'] = "视频列表"
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
            qvideos = Video.objects.filter(author_id=u.id)
            paginator = Pagination(qvideos, f'/up/{str(args[0])}?')
            props['videos'] = paginator.getPageSrc(page)
            props['pagination'] = paginator.getPage(page)
            props['page'] = {}
            props['page']['head'] = "UP 详情"
            return props
        else:
            return {}
    else:
        START_TIME = time.time()
        if mode == 0:
            q = Up.objects.filter()
            paginator = Pagination(q, "/upList?", length=q.count())
        elif mode == 1:
            q = Up.objects.filter(
                Q(username__contains=args[0]) | Q(signature__contains=args[0]))
            paginator = Pagination(
                q, "/search?type=up&keyword="+args[0], length=q.count())
        else:
            return

        ups = paginator.getPageSrc(page)
        END_TIME = time.time()

        props = {"authors": ups,
                 "pagination": paginator.getPage(page)}
        props['page'] = {}
        if mode == 1:
            if props['pagination'] != {}:
                props['page'][
                    'title'] = f"搜索完成，共计 {props['pagination']['count']} 条搜索结果，用时 {round(END_TIME-START_TIME, 6)} 秒."
            else:
                props['page']['title'] = f"搜索完成，无搜索结果，用时 {round(END_TIME-START_TIME, 6)} 秒."
            props['page']['head'] = "UP 搜索"
        else:
            props['page']['head'] = "UP 列表"

        return props
