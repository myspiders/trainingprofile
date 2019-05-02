# -*- coding: utf-8 -*-
import scrapy
from dateutil.parser import parse
import re
from guba.items import GubaItem
import pandas as pd
import os
class LunwenSpider(scrapy.Spider):
    name = 'lunwen'
    allowed_domains = ['guba.eastmoney.com']
#    start_urls = ['http://guba.eastmoney.com/']
    os.chdir('D:\\日回报率文件')
    index=pd.read_excel('上市股票一览.xlsx',sheet_name=1)
    start_stck=list(index.代码)
#    start_stck=['600519']#list(data['品种代码'])
    
    def start_requests(self):
        for stck_nuber in self.start_stck:
            number=re.findall('(\d+).\w',stck_nuber)
            for i in range(1,50):
                url='http://guba.eastmoney.com/list,'+str(number[0])+',1,f_'+str(i)+'.html'
                yield scrapy.Request(url,callback=self.parse_next,meta={'stck':number[0]},dont_filter=True)
    def parse_next(self,response):
        title1=response.xpath('//div[@class="articleh normal_post"]')
        stck1=response.meta['stck']
        for div in title1:
            link1=div.xpath('./span[3]/a/@href').extract_first()
            counts=div.xpath('./span[2]/text()').extract_first()
            reads=div.xpath('./span[1]/text()').extract_first()
            date=div.xpath('./span[5]/text()').extract_first()
            newsid=re.findall('news,\d+,(\d+).html',link1)
            link='http://guba.eastmoney.com'+link1
            if parse('3-1')<=parse(date)<=parse('4-30'):
                link2=re.findall('(.*).html',link1)
 #               print(link2[0],link)
 #               print(newsid)
                yield scrapy.Request(link,callback=self.next,meta={'stck1':stck1,'link2':link2[0],'reads':reads,'newsid1':newsid[0],'counts':counts})
    def next(self,response):
        stck2=response.meta['stck1']
        title1=response.xpath('//div[@id="zwconttbt"]/text()').extract()[0]
        link3=response.meta['link2']
        reads1=response.meta['reads']
        newsid2=response.meta['newsid1']
        time1=response.xpath('//div[@id="zwconttb"]//div[@class="zwfbtime"]/text()').re('发表于 ?(.*) 股吧网页版')[0]
        if parse(time1)>parse('2016-1-1'):
            text=','.join(response.xpath('//div[@id="zw_body"]//p/text()').extract()).strip()
            origin=response.xpath('//*[@id="zw_header"]//text()').extract()[0]
            origin1=re.sub('作者：.*','',origin)
            origin2=re.findall('来源：(.*)',origin1)
#            pinglv=response.xpath('//div[@id="zwlist"]/div[@class="zwli clearfix"]')
 #           print(origin2)
            page=response.xpath('//div[@id="zwcontab"]//span[@class="comment_num"]/text()').extract()
            if page!=[]:
               page1=re.findall('\W(\d+)\W',page[0])
               page2=int(int(page1[0])/30)+2
               for i in range(1,page2):
                    pagelink='http://guba.eastmoney.com'+link3+'_'+str(i)+'.html'
                    yield scrapy.Request(pagelink,callback=self.cri,meta={'stck2':stck2,'reads1':reads1,'newsid2':newsid2,'title1':title1,'text1':text,'origin2':origin2[0],'cri_counts':page1[0],'time1':time1})
    def cri(self,response):
        item=GubaItem()
        stck3=response.meta['stck2']
        title2=response.meta['title1']
        time2=response.meta['time1']
        text2=response.meta['text1']
        origin3=response.meta['origin2']
        cri_counts1=response.meta['cri_counts']
        reads2=response.meta['reads1']
        newsid3=response.meta['newsid2']
        item=GubaItem()
        pinglv=response.xpath('//div[@id="zwlist"]/div[@class="zwli clearfix"]')
        for cri in pinglv:
            item['stck']=stck3
            item['title']=re.sub(" ","",title2)
            item['time1']=time2
            item['text']=text2
            item['nickname']=cri.xpath('.//div[@class="zwlianame"]/span/a/text()').extract_first()
            item['time2']=cri.xpath('.//div[@class="zwlitime"]/text()').re('发表于 (.*)')[0]
            item['content']=cri.xpath('.//div[@class="short_text"]/text()').extract()[0]
            item['origin']=origin3
            item['cri_counts']=cri_counts1
            item['reads']=reads2
            item['newsid']=newsid3
            yield item
            