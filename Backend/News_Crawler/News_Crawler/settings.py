# -*- coding: utf-8 -*-

# Scrapy settings for News_Crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random

##############################

# Setting your MySQL connection info here

TABLE_NAME = 'netfin_source_message'
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'netfin_source_message'
MYSQL_USER = 'root'
MYSQL_PASSWD = '1403'
MYSQL_PORT = 3306


'''
TABLE_NAME = 'netfin_source_message'
MYSQL_HOST = '10.2.17.208'
MYSQL_DBNAME = 'financial'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'mysql'
MYSQL_PORT = 3306
'''

###############################

# Path of the Stopwords and target Corpora

path_Target = 'spiders/Target'
path_Stopwords = 'spiders/stopwords.txt'

################################

# Parameters of scrapy

IsHeadless = True    # True when using PhantomJS
thres = 0.2          # Threshold for filtering articles according to text similarity
page = 2               # How many pages of information do we need

name = 'News_Crawler'
allowed_domains = ['https://new.qq.com/']

# Choose your websites list

start_urls = [
    'https://new.qq.com/ch/tech/',  # Tencent Tech URL
    'https://new.qq.com/ch2/ai',  # Tencent AI URL
    #'https://new.qq.com/ch2/internet',  # Tencent Internet URL
    #'https://new.qq.com/ch2/bt',  # Tencent frontier tech URL
    #'https://new.qq.com/ch2/tcctit',  # Tencent TCCTIT URL
    # 'https://new.qq.com/tag/276813',     #Tencent BlockChain URL
    # 'https://new.qq.com/ch2/tech_cycx'   #Tencent tech innovation URL
]

keyword = 3
abstract = 3


#############################
# Set up the docker for splash first
# docker pull scrapinghub/splash
# docker run -p 8050:8050 scrapinghub/splash
# Then your SPLASH_URL is your localhost + 8050 portal

SPLASH_URL = 'http://localhost:8050/'

##############################

# Following are settings that automatically created by Scrapy framework, some basic settings

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

ITEM_PIPELINES = {
        'News_Crawler.pipelines.News_CrawlerPipeline':300
        }
BOT_NAME = 'News_Crawler'

SPIDER_MODULES = ['News_Crawler.spiders']
NEWSPIDER_MODULE = 'News_Crawler.spiders'


##################################################

DOWNLOAD_MAXSIZE = 10737418240

CLOSESPIDER_TIMEOUT = 10000
DOWNLOAD_TIMEOUT = 20

ROBOTSTXT_OBEY = True  # Obey anti-scraping roles

DOWNLOAD_DELAY = random.randint(1, 3)  # Avoiding anti-scraping
RETRY_ENABLED = False
#RETRY_TIMES = 5

COOKIES_ENABLED = False # Avoid using same cookies
REDIRECT_ENABLED = False

LOG_LEVEL = 'ERROR'
#################################################
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    # UA pools
    'News_Crawler.middlewares.RandomUserAgent': 1,
    'News_Crawler.middlewares.ProxyMiddleware': 100,
    # JS
     'News_Crawler.middlewares.PhantomJSMiddleware': 80,
    # 'News_Crawler.middlewares.SeleniumMiddleware': 55,


   # 'scrapy_splash.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
}


SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

##########################################################

DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

PROXIES = [
    {'ip_port': '111.11.228.75:80', 'user_pass': ''},
    {'ip_port': '120.198.243.22:80', 'user_pass': ''},
    {'ip_port': '111.8.60.9:8123', 'user_pass': ''},
    {'ip_port': '101.71.27.120:80', 'user_pass': ''},
    {'ip_port': '122.96.59.104:80', 'user_pass': ''},
    {'ip_port': '122.224.249.122:8088', 'user_pass': ''},
]