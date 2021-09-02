import os
import json
from numpy.core.fromnumeric import sort
import pandas
import datetime
from matplotlib import pyplot as plt
import numpy as np

# - -1. global variables
videos = 0
tags = 0
ups = 0

# - 0. Write Crawlled Result to Dataframe
# --|  videos
# --|  authors
# --|  tags


def GetDataframe():
    global videos, tags, ups
    videos = pandas.read_sql_table(
        'Web_video', "sqlite:///Database/db.sqlite3")
    tags = pandas.read_sql_table('Web_tag', "sqlite:///Database/db.sqlite3")
    ups = pandas.read_sql_table('Web_up', "sqlite:///Database/db.sqlite3")

# - 1. Calculate growth speed of video amount


def Conclusion1():
    idList = np.array(videos['id'])
    timeList = list(videos['uploadTime'])
    timeList = np.array(list(map(lambda x: x.timestamp(), timeList)))
    idRepresent = idList // 1000000

    # Paint Graphs Preparation
    x = []
    x_label = []
    y = []
    y2 = []

    # Calc average time for each uniqueId
    idUnique = np.unique(idRepresent)
    for tid in idUnique:
        mask = (idRepresent == tid)
        averageTime = np.dot(mask, timeList) // mask.sum()
        x.append((datetime.datetime.fromtimestamp(averageTime) -
                  datetime.datetime.fromtimestamp(1388505600)).days // 30)  # 2014-1-1 00:00:00
        x_label.append(datetime.datetime.fromtimestamp(
            averageTime).strftime('%Y/%m'))
        y2.append(mask.sum())

    y = idUnique
    y2 = np.array(y2) / np.array([1100, 1499, 1499,
                                  1499, 1499, 1499, 1499, 1499, 1499, 1499]) * 100

    # Calc x-id and x-label
    # Start 2014.01 <-> 1, with month as unit
    # print(x)
    # print(y)
    # print(x_label)
    plt.rcParams['savefig.dpi'] = 300
    plt.suptitle('上传视频量与审核通过率')

    # Draw graph 1
    plt.subplot(2, 1, 1)
    plt.plot(x, y)

    # Chinese tags support and minus symbol, reference https://blog.csdn.net/qq_40563761/article/details/102989770
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.ylabel('总视频上传量 / M')

    plt.xticks(x, x_label, rotation=315)
    plt.yticks(np.arange(5, 95, 10))

    # plt.savefig('1-1.png')
    # plt.close()

    # Draw graph 2
    plt.subplot(2, 1, 2)
    plt.plot(x, y2, 'D')

    plt.ylabel('上传视频存活率 / %')

    plt.xticks(x, x_label, rotation=315)
    plt.ylim(30, 60)

    # Save Figure
    plt.tight_layout()
    plt.savefig('1.png')
    plt.close()

# - 2. Found most popular tags


def Conclusion2():
    frequencies = {}  # 2014~2020, all
    frequencies['all'] = {}
    frequenciesWithHits = {}  # 2014~2020, all
    frequenciesWithHits['all'] = {}
    # print(frequencies)

    for index, row in videos.iterrows():
        id = (row['id'])
        uploadYear = str(row['uploadTime'].year)
        hits = row['playCount']

        # Find tags related to id
        relatedTags = tags[tags['video_id'] == id]
        for index, tagRow in relatedTags.iterrows():
            tagName = tagRow['tagName']

            # Push Tagname to frequencies list
            if uploadYear not in frequencies:
                frequencies[uploadYear] = {}
                frequenciesWithHits[uploadYear] = {}
            if tagName not in frequencies[uploadYear]:
                frequencies[uploadYear][tagName] = 0
                frequenciesWithHits[uploadYear][tagName] = 0
            if tagName not in frequenciesWithHits['all']:
                frequenciesWithHits['all'][tagName] = 0
            if tagName not in frequencies['all']:
                frequencies['all'][tagName] = 0

            frequencies[uploadYear][tagName] += 1
            frequencies['all'][tagName] += 1
            frequenciesWithHits[uploadYear][tagName] += hits
            frequenciesWithHits['all'][tagName] += hits

    # Carry out sort in frequencies dict and truncate top 10 tags
    for key in frequencies.keys():
        frequencies[key] = sorted(
            frequencies[key].items(), key=lambda x: x[1], reverse=True)[0:10]
    for key in frequenciesWithHits.keys():
        frequenciesWithHits[key] = sorted(
            frequenciesWithHits[key].items(), key=lambda x: x[1], reverse=True)[0:10]

    # print(frequencies)
    # print(frequenciesWithHits)

    # Draw Graph 1
    plt.rcParams['savefig.dpi'] = 300
    plt.suptitle('视频标签频率表')
    k = 0
    for key in frequencies.keys():
        k += 1
        plt.subplot(2, 4, k)
        if key == "all":
            plt.title('Overall')
        else:
            plt.title(key)
        plt.bar(np.arange(1, 11, 1), list(
            map(lambda x: x[1], frequencies[key])))
        plt.xticks(np.arange(1, 11, 1), list(
            map(lambda x: x[0], frequencies[key])), rotation=270, fontsize=6)
        plt.ylabel('视频数')

    # Save Figure
    plt.tight_layout()
    plt.savefig('2-1.png')
    plt.close()

    # Draw Graph 2
    plt.rcParams['savefig.dpi'] = 300
    plt.suptitle('播放量标签频率表')
    k = 0
    for key in frequenciesWithHits.keys():
        k += 1
        plt.subplot(2, 4, k)
        if key == "all":
            plt.title('Overall')
        else:
            plt.title(key)
        plt.bar(np.arange(1, 11, 1), list(
            map(lambda x: x[1]//100000, frequenciesWithHits[key])))
        plt.xticks(np.arange(1, 11, 1), list(
            map(lambda x: x[0], frequenciesWithHits[key])), rotation=270, fontsize=6)
        plt.ylabel('播放量 / 100k')

    # Save Figure
    plt.tight_layout()
    plt.savefig('2-2.png')
    plt.close()


# - 3. Find the relationship between the author's level and the author's follower count
def Conclusion3():

    # Get author follower rank
    def getRank(n):
        checkpoint = [0, 2000, 10000, 50000, 200000, 1145141919810]
        for i in range(1, 6):
            if (checkpoint[i-1] <= n < checkpoint[i]):
                return i
        return -1

    LevelFrequencies = {}
    LevelFrequencies['all'] = [0, 0, 0, 0, 0, 0, 0]

    for index, row in ups.iterrows():
        lvl = row['level']
        rawFollowerCount = row['followerCount']
        if rawFollowerCount[-1] != '万':
            follower = int(rawFollowerCount)
        else:
            follower = int(float(rawFollowerCount[:-1]) * 10000)
        rank = str(getRank(follower))

        # Push to dict
        if not rank in LevelFrequencies:
            LevelFrequencies[rank] = [0, 0, 0, 0, 0, 0, 0]
        LevelFrequencies[rank][lvl] += 1
        LevelFrequencies['all'][lvl] += 1

    # print(LevelFrequencies)

    # Paint Figure
    plt.rcParams['savefig.dpi'] = 300
    plt.suptitle('UP 主等级与粉丝数')

    i = 0
    for key in sorted(LevelFrequencies.keys()):
        i += 1
        plt.subplot(2, 3, i)

        # Set subfigure title
        if key == 'all':
            plt.title('Overall')
        elif key == '1':
            plt.title('[0, 2k)')
        elif key == '2':
            plt.title('[2k, 10k)')
        elif key == '3':
            plt.title('[10k, 50k)')
        elif key == '4':
            plt.title('[50k, 200k)')
        elif key == '5':
            plt.title('[200k, INF)')

        labels = ['Lv. ' + str(i) for i in range(0, 7)]
        plt.pie(LevelFrequencies[key], wedgeprops={
                'edgecolor': 'black', 
                'linewidth': '0.4'
                }, textprops={'color': 'white'}, labels=labels)
    plt.legend(prop={'size': 6}, bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)

    # Save Figure
    plt.tight_layout()
    plt.savefig('3.png')
    plt.close()


if __name__ == "__main__":
    GetDataframe()
    Conclusion1()
    Conclusion2()
    Conclusion3()
