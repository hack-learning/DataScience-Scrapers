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
    def __init__(self, db, user, passwd, host,port):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port

    def process_item(self, item, spider):
        
        if item.get('badge_url'):
            
            self.cursor.execute('CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTO_INCREMENT,title VARCHAR(100), \
                                badge_url VARCHAR(255) UNIQUE, url VARCHAR(255), overview TEXT)')
            sql = 'INSERT INTO courses(title, badge_url, url, overview) VALUES ("{title}", "{badge_url}", "{url}", "{overview}")'.format(**item)
        else:
            
            #domain_query
            query_1 = "SELECT id FROM domains WHERE domain_name='"+spider.allowed_domains[0]+"'"            
            self.cursor.execute(query_1)
            id_domains = self.cursor.fetchall()
            id_domain = id_domains[0][0]            
            
            #Insert scraped information to the tables
            self.cursor.execute('CREATE TABLE IF NOT EXISTS \
                articles (id INTEGER PRIMARY KEY AUTO_INCREMENT,\
                id_domain INTEGER, FOREIGN KEY (id_domain) \
                REFERENCES domains (id), title VARCHAR(100), overview TEXT,\
                url VARCHAR(255) UNIQUE,\
                image_url VARCHAR(255), body TEXT, pub_date DATE)')
            sql = "INSERT INTO articles(\
                id_domain, title, overview, url, image_url, body, pub_date) VALUES \
                ({id_domain},'{title}', '{overview}', '{url}', '{image_url}', '{body}',\
                 '{pub_date}')".format(**item, id_domain=id_domain)
        try:
            
            self.cursor.execute(sql)
            self.conn.commit()
        except mysql.connector.IntegrityError as err:
            print('Article already in the DataBase.')
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
                port=self.port,
                auth_plugin='mysql_native_password'
                )
        self.cursor = self.conn.cursor()
        print('Connection succesfull')

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
        port = db_settings['port']
        return cls(db, user, passwd, host,port)

