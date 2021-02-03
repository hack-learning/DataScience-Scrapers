# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from itemadapter import ItemAdapter
from scrapy.exceptions import NotConfigured


class NewsScraperPipeline:
    def process_item(self, item, spider):
        return item


class DataBasePipeline(object):
    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    def process_item(self, item, spider):
        if item.get('badge_url'):
            sql = 'INSERT INTO courses(title, badge_url, url, overview) VALUES ("{title}", "{badge_url}", "{url}", "{overview}")'.format(**item)
        else:
            sql = 'INSERT INTO articles(title, overview, url, image_url, body, pub_date) VALUES ("{title}", "{overview}", "{url}", "{image_url}", "{body}", "{pub_date}")'.format(**item)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
        return item

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
                db=self.db,
                user=self.user,
                host=self.host,
                passwd=self.passwd,
                charset='utf8',
                use_unicode=True,
                auth_plugin='mysql_native_password'
                )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict('DB_SETTINGS')
        if not db_settings:
            raise NotConfigured
        db = db_settings['db']
        passwd = db_settings['passwd']
        user = db_settings['user']
        host = db_settings['host']
        return cls(db, user, passwd, host)

