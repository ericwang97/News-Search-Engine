# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from imp import reload
from scrapy_splash import SplashRequest
from scrapy.http import Request
from scrapy.selector import Selector
from News_Crawler.items import News_CrawlerItem
from News_Crawler.textrank4zh import TextRank4Keyword, TextRank4Sentence
import sys
import time
import News_Crawler.settings as settings
import News_Crawler.spiders.similarity as similarity
reload(sys)

class SplashSpider(Spider):

    IsHeadless = settings.IsHeadless
    thres = settings.thres

    name = settings.name
    allowed_domains = settings.allowed_domains
    start_urls = settings.start_urls

    scan_id = str(round(time.time()))
    s = similarity.TextSimilarity(settings.path_Target,settings.path_Stopwords)  # Read all Target CORPORA and Stop words lists

    def start_requests(self):


        for url in self.start_urls:
            print('---------------------------------------------------------------------------Start Parsing %s -------------------------------------------------------------------------------'% url)

            if self.IsHeadless:

                yield Request(url, callback=self.parse_URL, dont_filter=True, meta={
                    'Headless': True, 'dont_redirect': True,
                    'splash': {
                        'args': {'wait': '0.5'}
                        , 'endpoint': 'execute'}
                })

            else:

                yield Request(url, callback=self.parse_URL, dont_filter=True, meta={
                    'GoogleChrome': True, 'dont_redirect': True,
                    'splash': {
                        'args': {'wait': '0.5',  'images': 0}
                        , 'endpoint': 'execute'}
                })


    def parse_URL(self, response):          # Parsing each web page and get all articles under this page!

        site = Selector(response)
        time.sleep(10)                      # Longer time break

        URL_site = site.xpath('//h3[@class]/a[@target="_blank"]/@href').extract()
        url_title = site.xpath('//h3[@class]/a[@target="_blank"]/text()').extract()
        print('-' * 100)
        print('Parsing URL：',response.url)
        print('Number of News：', len(URL_site))
        print('-' * 100)

        for j in range(0, len(URL_site)):

            strtitle = url_title[j]
            strurl = URL_site[j]
            keywords = site.xpath('//div[(@class = "detail") and (h3/a/@href = "{}")]/div[@class="tags"]'
                                  '//a[@class = "tag"]/text()'.format(strurl)).extract()
            print('''index：{} title：{} Keywords: {} URL：{} FROM WEB：{}'''.format((j+1),strtitle,','.join(keywords),strurl,response.url))

            if response.url == 'https://new.qq.com/ch/tech/':
                net_name = 'Tencent Tech'#'科技-腾讯网'
            elif response.url == 'https://new.qq.com/ch2/ai':
                net_name = 'Tencent AI' #'人工智能-腾讯网'
            elif response.url == 'https://new.qq.com/ch2/internet':
                net_name = 'Tencent Internet'  #'互联网-腾讯网'
            elif response.url == 'https://new.qq.com/ch2/bt':
                net_name = 'Tencent frontier tech' #'前沿科技-腾讯网'
            elif response.url == 'https://new.qq.com/ch2/tcctit':
                net_name = 'Tencent TCCTIT'  #'通信/传统IT-腾讯网'
            elif response.url == 'https://new.qq.com/ch2/tech_cycx':
                net_name = 'Tencent tech innovation' #'创业创新-腾讯网'
            elif response.url == 'https://new.qq.com/tag/276813':
                net_name = 'Tencent BlockChain' #'区块链-腾讯网'
            else:
                pass
            item = News_CrawlerItem()
            item['net_name'] = net_name
            item['keyword'] = keywords

            yield SplashRequest(strurl,self.parse_article,
                                args={'wait': '0.5'},dont_filter=True, meta={'item':item})


    def parse_article(self, response):  # Parsing each article!!!
        try:
            site = Selector(response)

            #Title
            title = site.xpath('//div[@class="LEFT"]/h1/text()').extract()
            url = response.url

            # Time
            year = site.xpath('//div[@class="year through"]/span/text()').extract()
            md = site.xpath('//div[@class="md"]/text()').extract()
            hm = site.xpath('//div[@class="time"]/text()').extract()
            ent_time = str(year[0])+'/'+str(md[0])+'/'+str(md[2])+' '+str(hm[0])+':'+str(hm[2])
            hot_degree = site.xpath('//div[@class="text"]/i[@id="cmtNum"]/text()').extract()

            # Article
            raw_article =site.xpath('//p[@class="one-p"]/text()').extract()
            content =''

            print('Title:%s ' % title[0])
            print('URL:%s ' % url)
            print('Time:%s ' % ent_time)
            print('Comment Number:%s ' % hot_degree[0])

            for va in raw_article[0:-2]:
                content += va

            # Keywords and Abstract
            raw_keywords,raw_abstract = text_keyword_abstract(content, settings.keyword, settings.abstract)  # Number of Keywords and Abstract

            keywords = response.meta['item']['keyword']


            simi = self.s.cal_similarities(content)  # Calculate the similarities and return the similarity list

            digest = ''
            for va in raw_abstract:
                digest += va

            print('Keywords:%s ' % ' '.join(keywords))

            print('Abstract:%s ' % digest)
            #print('Article:%s ' % content)
            print('Similarity:', simi)


        ########################################################


            if len(keywords)>0 and len(digest)>0:

                if max(simi) > self.thres:

                    item = News_CrawlerItem()

                    item['title'] = title[0]
                    item['hot_degree'] = hot_degree[0]
                    item['net_name'] = response.meta['item']['net_name']
                    item['digest'] = digest
                    item['keyword'] = ' '.join(keywords)
                    item['url'] = url
                    item['ent_time'] = ent_time
                    item['scan_id'] = self.scan_id
                    item['content'] = content
                    yield item

                    print('-----------------------------------------------------------------------------------------------------------------')

                else:
                    print('Article is not related (similarity < threshold), pass')
                    print('-----------------------------------------------------------------------------------------------------------------')
                    pass
            else:
                print('Article is not related (similarity < threshold), pass')
                print('-----------------------------------------------------------------------------------------------------------------')
                pass

        except:
            print('Unable to parse this article, go to the next one')
            print('-----------------------------------------------------------------------------------------------------------------')
            pass

def text_keyword_abstract(article, keywords_len, sentences_len):

    tr4w = TextRank4Keyword()
    tr4w.analyze(text=article, lower=True, window=2)
    keywords = []
    for item in tr4w.get_keywords(keywords_len, word_min_len=2):
        keywords.append(item.word)
    keywords = ' '.join(keywords)

    sentences = article.split('。')
    first_sentence = sentences[0]
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=article, lower=True, source='all_filters')
    abstract = []
    for item in tr4s.get_key_sentences(num=sentences_len):
        if item.sentence != first_sentence:
            abstract.append(item.sentence+ '。')
    abstract = '\n'.join(abstract)
    return keywords,abstract






