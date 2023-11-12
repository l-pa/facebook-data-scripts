import json
import sys
import re
import datetime
from urllib.request import urlopen
from lxml import etree
from itertools import islice


filename = sys.argv[1]  # first argument as filename

# or change filename to 'message.json'
file = open(filename, 'r', encoding='utf8')

jsonToFix = json.load(file)

# Count every word

messagesAll = {}
messagesA = {}
messagesB = {}

for i in jsonToFix['messages']:
    try:
        tmp = []
       # tmp = re.findall(r"[\w']+", i['content'])
        tmp = i['content'].split()
        for word in tmp:

            if word in messagesAll:
                messagesAll[word] += 1
            else:
                messagesAll[word] = 1

            if i['sender_name'] == jsonToFix['title']:
                if word in messagesA:
                    messagesA[word] += 1
                else:
                    messagesA[word] = 1
            else:
                if word in messagesB:
                    messagesB[word] += 1
                else:
                    messagesB[word] = 1

    except Exception:
        pass

sortedAll = sorted(messagesAll.items(), key=lambda kv: kv[1], reverse=True)
sortedA = sorted(messagesA.items(), key=lambda kv: kv[1], reverse=True)
sortedB = sorted(messagesB.items(), key=lambda kv: kv[1], reverse=True)

# %Y-%m-%d %H:%M:%S

# Get youtube videos from your conversation and their titles


def get_youtube_titles_from_conversation():
    videoCount = 0
    for i in jsonToFix['messages']:
        try:
            tmp = []
            tmp = i['content'].split()
            for word in tmp:
                if 'youtube.com/watch' in word:
                    try:
                        youtube = etree.HTML(urlopen(word).read())
                        video_title = youtube.xpath(
                            "//span[@id='eow-title']/@title")
                    except Exception as e:
                        print(e)
                        video_title = 'Error'

                    print('{} -> {}'.format(word, video_title))
                    videoCount += 1
        except Exception:
            pass


def first_n_from_iterable(n, iterable):
    """Return first n items of the iterable as a list"""
    return list(islice(iterable, n))


def get_top_messages_per_sender(dictA, dictB={}, n=10):
    """Return first n messages per sender"""

    print('\nTop {} from : {}'.format(n, jsonToFix['title']))
    for key in first_n_from_iterable(n, dictA):
        print(key)

    print('\nYour top {} '.format(n))
    for key in first_n_from_iterable(n, dictB):
        print(key)


def get_top_messages(dict_msgs, n=10):
    """Return first n messages of dict"""

    print('\nTop {} :'.format(n))
    for key in first_n_from_iterable(n, dict_msgs):
        print(key)

# datetime.datetime.fromtimestamp(float(i['timestamp_ms']) / 1000.0).strftime('%B-%Y')


def get_top_per_month(n=10):
    count = 0
    tmp_dic = {}
    messages_per_month = 0
    for i in jsonToFix['messages']:
        try:
            if str(datetime.datetime.fromtimestamp(float(jsonToFix['messages'][count]['timestamp_ms']) / 1000.0).strftime('%Y-%B')) == str(datetime.datetime.fromtimestamp(float(jsonToFix['messages'][count+1]['timestamp_ms']) / 1000.0).strftime('%Y-%B')):
                messages_per_month += 1
                tmp = []
                tmp = i['content'].split()
                for word in tmp:
                    if word in tmp_dic:
                        tmp_dic[word] += 1
                    else:
                        tmp_dic[word] = 1

            else:
                pass
                print('{} | {}'.format(datetime.datetime.fromtimestamp(
                    float(i['timestamp_ms']) / 1000.0).strftime('%Y-%B'), messages_per_month))

                sorted_month = sorted(
                    tmp_dic.items(), key=lambda kv: kv[1], reverse=True)

                for key in first_n_from_iterable(n, sorted_month):
                    print(key)

                messages_per_month = 0
                tmp_dic = {}
                sorted_month = {}
            count += 1
        except Exception:
            pass


if __name__ == '__main__':
    get_top_per_month()
