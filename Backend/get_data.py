import requests
import mysql.connector
import schedule
import sqlalchemy
import time

from load import MainLoad
from twitter import getTweet


def writeSQL(dataDF, table):
    connect = sqlalchemy.create_engine('mysql+pymysql://'
                                       'inf551:inf551@127.0.0.1:3306/'
                                       'news', encoding='utf8')

    dataDF.to_sql(name=table, con=connect, if_exists='append', index=False,
                  dtype={'user_name': sqlalchemy.types.VARCHAR(45),
                         'created_time': sqlalchemy.types.DATETIME,
                         'favorite_count': sqlalchemy.types.INT,
                         'keywords': sqlalchemy.types.TEXT,
                         'url': sqlalchemy.types.VARCHAR(45),
                         'text': sqlalchemy.types.TEXT,
                         'topic': sqlalchemy.types.VARCHAR(45),
                         'scan_time': sqlalchemy.types.VARCHAR(45)})


def getExistedData(connect, table):

    source_urlselect = '''select user_name, created_time from news.{}'''.format(table)
    data_list = []
    cursor = connect.cursor()
    cursor.execute(source_urlselect)
    for r in cursor:
        name = r[0]
        time = r[1].strftime('%H:%M:%S %b %d %Y')
        data_list.append((name, time))
    cursor.close()

    return set(data_list)


def main():

    connect = mysql.connector.connect(
        host='127.0.0.1',
        user='inf551',
        passwd='inf551',
        port=3306,
        charset='utf8',
        use_unicode=True)

    data_list = getExistedData(connect, table='tweet')
    firebaseURL = 'https://inf551-a79f9.firebaseio.com/'
    requests.request('PUT', firebaseURL + 'news.json', json={})
    requests.request('PUT', firebaseURL + 'newsAllDataNode.json', json={})
    requests.request('PUT', firebaseURL + 'newsNode.json', json={})

    topic_list = ['Trump', 'China', 'HongKong', 'COVID', 'Finance', 'Computer Science', 'Amazon',
                  'Software Engineering', 'Machine Learning']

    print('------------------ Start Scanning, end time: {} ---------------------'.format(
        time.asctime(time.localtime(time.time()))))

    print('------- Start getting tweets -------')
    for topic in topic_list:
        dataDF = getTweet(data_list, topic=topic, total_num=10, result_type='popular',
                      language='en', keywords_num=2, abstract_num=1)
        writeSQL(dataDF, table='tweet')

    MainLoad(firebaseURL, connect, Mute=True, databaseNameList=['news'])

    print('------------------ Scanning is done, end time: {} ---------------------'.format(
        time.asctime(time.localtime(time.time()))))

    connect.close()

if __name__ == "__main__":

    run_schedule = True

    if run_schedule:
        #schedule.every(0.2).minutes.do(main)
        schedule.every().hour.do(main)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        main()
