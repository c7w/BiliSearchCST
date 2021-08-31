from bs4 import BeautifulSoup
import requests
import time
import sys
import re
from selenium import webdriver
from datetime import datetime
import json
from selenium.webdriver.chrome.options import Options


def parsePage(id, soup):

    try:

        # Title and abstract
        title = soup.h1['title']
        abstract = soup.find('div', class_='desc-info').get_text()

        # UploadTime, PlayCount, BulletCount, CommentCount
        video_data = soup.find('div', class_='video-data').contents
        uploadTime = datetime.strptime(
            video_data[2].get_text(), '%Y-%m-%d %H:%M:%S')
        playCount = int(video_data[0]['title'][4:])
        bulletCommentCount = int(video_data[1]['title'][7:])

        # ImageURL
        imageUrl = soup.head.find('meta', itemprop='image')['content']

        # Feedback
        ops = soup.find('div', class_='ops').contents
        feedback = {}
        feedback['like'] = ops[4].get_text().strip()

        feedback['coin'] = ops[5].get_text().strip()
        feedback['star'] = ops[6].get_text().strip()

        feedback['share'] = ops[7].get_text().split('\n')[0].strip()
        if (feedback['like'] == '点赞'):
            feedback['like'] = '0'
        if (feedback['coin'] == '投币'):
            feedback['coin'] = '0'
        if (feedback['star'] == '收藏'):
            feedback['star'] = '0'
        if (feedback['share'] == '分享'):
            feedback['share'] = '0'

        # Author ID
        name = soup.find('div', class_='name')
        sel = re.compile('href="//space.bilibili.com/(.*?)"')
        authorId = int(re.findall(sel, str(name))[0])

        # Comment
        commentCount = int(
            soup.find('span', class_='b-head-t results').get_text())
        commentList = soup.find('div', class_='comment-list')
        commentGroup = commentList.find_all(
            'div', class_='list-item reply-wrap')
        comments = []
        for comment in commentGroup:
            # Push to comments
            comments.append(comment.find('div', class_='con').p.get_text())
            if (len(comments) == 5):
                break

        # Tags
        tags = []
        tagList = soup.find('ul', class_="tag-area clearfix")
        tagGroup = tagList.find_all('li', class_='tag')
        for tag in tagGroup:
            tags.append(tag.get_text().strip())

        resultData = {
            'id': id,
            'title': title,
            'abstract': abstract,
            'authorId': authorId,
            'uploadTime': uploadTime.timestamp(),
            'playCount': playCount,
            'commentCount': commentCount,
            'bulletCommentCount': bulletCommentCount,
            'imageUrl': imageUrl,
            'feedback': feedback,
            'comments': comments,
            'tags': tags
        }
        f = open(f"./CrawlResult/{str(id)}.json", 'w+', encoding='utf-8')
        json.dump(resultData, f, ensure_ascii=False, indent=4)
        f.close()
    except:
        pass


def getVideo(i):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-gpu')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('window-size=1920x5000')  # to load comments
    chrome_options.add_argument('log-level=3')
    driver = webdriver.Chrome(
        './webdriver/chromedriver.exe', options=chrome_options)

    base_url = 'https://www.bilibili.com/video/av' + str(i)
    driver.get(base_url + "/")
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    parsePage(i, soup)
    driver.quit()


if __name__ == "__main__":
    #1005680, 1006780
    
    for i in range(int(sys.argv[1]), int(sys.argv[2])):
        print("-----------------------------")
        print(str(i))
        getVideo(i)
        print("-----------------------------")
