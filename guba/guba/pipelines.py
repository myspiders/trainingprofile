# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import re
class MysqlPipeline(object):
    def __init__(self,host,user,password,database,port):
        self.host=host
        self.user=user
        self.password=password
        self.database=database
        self.port=port
    @classmethod
    def from_crawler(cls,crawler):
        return cls(host=crawler.settings.get('MYSQL_HOST'),
                    user=crawler.settings.get('MYSQL_USER'),
                    password=crawler.settings.get('MYSQL_PASSWORD'),
                    database=crawler.settings.get('MYSQL_DATABASE'),
                    port=crawler.settings.get('MYSQL_PORT'))
    def open_spider(self,spider):
        self.db=pymysql.connect(self.host,self.user,self.password,self.database,self.port,charset='utf8')
        self.cursor=self.db.cursor()
        print('数据连接成功')
    def close_spider(self,spider):
        self.db.close()
        
    def process_item(self, item, spider):
        data=dict(item)
        char=len(data)-1
        title_1=re.sub(" ","",item['title'])
        text_1=re.sub(" ","",item['text'])
        content_1=re.sub(" ","",item['content'])
#        keys=(title,time1,text,origin,stck,nickname,time2,content,cri_counts)
        values=','.join(['%s']*char)
        sql1='insert into lunwen(title,time1,newsid1,origin,stck,nickname,time2,content,cri_counts,reads1) values({values})'.format(values=values)
        sql2='insert into news(newsid1,text1) values(%s,%s)'
        sqldata1=(title_1,item['time1'],item['newsid'],item['origin'],item['stck'],item['nickname'],item['time2'],content_1,item['cri_counts'],item['reads'])
        sqldata2=(item['newsid'],text_1)
        try:
            self.cursor.execute(sql1,sqldata1)
            self.cursor.execute(sql2,sqldata2)
            self.db.commit()
            return print('储存成功')
        except:
            return print('失败')
class  CSVPipeline(object):
    pass
