import os, sys
import time
import json
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def parseHtml(id, soup):

    avatarUrl = 'https:' + soup.find('img', id='h-avatar')['src'].split('@')[0]
    username = soup.find('span', id='h-name').get_text()
    level = int(
        soup.find('a', href='//www.bilibili.com/html/help.html#k')['lvl'])
    signature = soup.find('h4', class_='h-sign')['title']
    followingCount = (soup.find(
        'p', class_='n-data-v space-attention').get_text().strip())
    followerCount = (soup.find(
        'p', class_='n-data-v space-fans').get_text().strip())

    resultData = {
        "id": id,
        "username": username,
        "signature": signature,
        "level": level,
        "avatarUrl": avatarUrl,
        "followerCount": followerCount,
        "followingCount": followingCount
    }

    f = open(f"./UpResult/{str(id)}.json", 'w+', encoding='utf-8')
    json.dump(resultData, f, ensure_ascii=False, indent=4)
    f.close()


def getUp(i):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-gpu')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('window-size=1920x5000')
    chrome_options.add_argument('log-level=3')
    driver = webdriver.Chrome(
        './webdriver/chromedriver.exe', options=chrome_options)

    base_url = 'https://space.bilibili.com/' + str(i)
    driver.get(base_url)
    time.sleep(0.5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    parseHtml(i, soup)


if __name__ == "__main__":
    #1005680, 1006780
    if sys.argv[1] == 'run':
        getUp(int(sys.argv[2]))
        exit(0)
    if sys.argv[1] == 'generate':
        # Read from json to the author set
        s = set()
        list_dir = os.listdir('./CrawlResult')
        for name in list_dir:
            f = open('./CrawlResult/' + name, 'r', encoding='utf-8')
            j = json.load(f)
            s.add(j['authorId'])
            f.close()
        
        thread = 30
        i = 0
        for item in s:
            f = open('./UpBash/' + str(i%thread) + '.bat', 'a+', encoding='utf-8')
            if i < thread:
                f.write('cd E:\Project\Homework\python\Crawler\n')
            f.write('python upInfo.py run ' + str(item) + '\n')
            f.close()
            i += 1
    if sys.argv[1] == 'check':
        list_dir = os.listdir('./CrawlResult')
        for name in list_dir:
            f = open('./CrawlResult/' + name, 'r', encoding='utf-8')
            j = json.load(f)
            if (j['authorId'] == int(sys.argv[2])):
                print(name)
            f.close()
    if sys.argv[1] == 'verify':
        list_dir = os.listdir('./CrawlResult')
        author_dir = os.listdir('./UpResult')
        check_list = []
        for name in list_dir:
            f = open('./CrawlResult/' + name, 'r', encoding='utf-8')
            j = json.load(f)
            if ( not (str(j['authorId']) + '.json' in author_dir)):
                check_list.append(name)
            f.close()
        print(check_list)
        print(len(check_list))
        
