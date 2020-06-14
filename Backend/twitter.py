# -*- coding:utf-8 -*-
from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterPager

import pandas as pd
from re import findall
import pytz
from tzlocal import get_localzone
from datetime import datetime
import time
from textrank4zh import TextRank4Keyword, TextRank4Sentence


def getTime(string):
    # weekday = string[0:3]
    string = string[4:-10] + string[-4:]
    time = datetime.strptime(string, '%b %d %H:%M:%S %Y')
    utc = pytz.utc
    tz = get_localzone()
    utc_dt = utc.localize(time)
    loc_dt = utc_dt.astimezone(tz)

    return loc_dt


def text_keyword_abstract(article, keywords_len, sentences_len):
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=article, lower=True, window=2)
    keywords = []
    for item in tr4w.get_keywords(keywords_len, word_min_len=2):
        keywords.append(item.word)
    keywords = ' '.join(keywords)

    sentences = article.split('.')
    first_sentence = sentences[0]
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=article, lower=True, source='all_filters')
    abstract = []
    for item in tr4s.get_key_sentences(num=sentences_len):
        if item.sentence != first_sentence:
            abstract.append(item.sentence + '.')
    abstract = '\n'.join(abstract)
    return keywords #, abstract


def searchTweet(data_list, topic, total_num, page_length, result_type, language, keywords_num, abstract_num,
                the_consumer_key, the_consumer_secret, the_access_token_key,
                the_access_token_secret):
    """
    搜索含有特定“内容”的推文
    :param abstract_num:
    :param keywords_num:
    :param language:
    :param result_type:
    :param topic:
    :param page_length:
    :param total_num:
    :param the_consumer_key: 已有的consumer_key
    :param the_consumer_secret: 已有的consumer_secret
    :param the_access_token_key: 已有的access_token_key
    :param the_access_token_secret: 已有的access_token_secret
    :return:
    """
    api = TwitterAPI(consumer_key=the_consumer_key,
                     consumer_secret=the_consumer_secret,
                     access_token_key=the_access_token_key,
                     access_token_secret=the_access_token_secret)
    result = TwitterPager(api, 'search/tweets', {'q': topic, 'count': page_length, 'result_type': result_type,
                                                 'lang': language})

    data = {}
    for i, item in enumerate(result.get_iterator()):
        try:
            if 'text' in item:
                time = getTime(item['created_at'])
                name = item['user']['screen_name']

                if (name, time.strftime('%H:%M:%S %b %d %Y')) not in data_list:
                    if 'favorite_count' not in item:
                        favorite = 0
                    else:
                        favorite = item['favorite_count']

                    text = item['text']
                    url = findall('[a-zA-z]+://[^\s]*', text)
                    if url:
                        url = url[0]
                    else:
                        url = ''

                    if item['entities']['hashtags']:
                        raw_keywords = ' '.join([each['text'] for each in item['entities']['hashtags']])
                    else:
                        raw_keywords = text_keyword_abstract(text, keywords_num, abstract_num)
                    data.update({i: [name, time, favorite, raw_keywords, url, text]})

            elif 'message' in item:
                print('ERROR %s: %s\n' % (item['code'], item['message']))
                continue
            if i >= total_num:
                break
        except:
            continue

    return data


def getTweet(data_list, topic, total_num, result_type, language, keywords_num, abstract_num):
    consumerKey = "lvf9g60mxvkheIQgZXJXbO8VS"
    consumerSecret = "d0t1A5MnCyNhWtmKeYc0y2xnNDQUAGsAmWKvmGwzyCmKxDb0Lf"
    accessToken = "1674933235-7En18Na7MqbUmSzVv45cJgcy0jIVHVHbcAQstJ0"
    accessTokenSecret = "cKRUu9se5PxKuzaCkTje2gUE5Vx0AIlq9JzP2l98dppEz"

    #print('------------------ Topic: {} ---------------------'.format(topic))

    data = searchTweet(data_list, topic=topic, total_num=total_num, result_type=result_type, language=language,
                       page_length=20, keywords_num=keywords_num, abstract_num=abstract_num,
                       the_consumer_key=consumerKey,
                       the_consumer_secret=consumerSecret,
                       the_access_token_key=accessToken,
                       the_access_token_secret=accessTokenSecret)
    dataDF = pd.DataFrame(data, index=['user_name', 'created_time', 'favorite_count', 'keywords', 'url', 'text']).T
    dataDF['topic'] = topic
    dataDF['scan_time'] = time.asctime(time.localtime(time.time()))

    #dataDF.to_csv('twitter.csv')

    return dataDF


