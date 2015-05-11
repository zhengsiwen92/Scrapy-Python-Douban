# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#import json
#import codecs
import MySQLdb as DB

class DoubanPipeline(object):
#    def __init__(self):
#        self.file=codecs.open('result_all.json','wb',encoding='utf-8')
#        
#    def process_item(self, item, spider):
##        This comment part is an alternative method: To make results shown in Chinese,not in ascii.
##        line=json.dumps(dict(item))+'\n'
##        self.file.write(line.decode("unicode_escape"))
#        line=json.dumps(dict(item),ensure_ascii=False)+'\n'
#        self.file.write(line)
#        return item
    con=DB.connect(host='localhost',user='root',passwd='4015',db='firstdb',charset="utf8")
    cur=con.cursor()
    def process_item(self, item, spider):
        sql="insert into groupinfo(groupname,groupurl) values('%s','%s')" % (''.join(item['GroupName']),''.join(item['GroupURL']))
        #sql="insert into groupinfo(groupname,groupurl) values('%s','%s')" % (''.join(item['GroupName']),item['GroupURL'])
        print sql
        try:
            self.cur.execute(sql)
            self.con.commit()   # this commit() command can't be omitted.
        except Exception,e:
            print  e
        return item