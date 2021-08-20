# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from mysql.connector.errors import Error
from itemadapter import ItemAdapter
from scrapy.exceptions import NotConfigured, DropItem


class NewsScraperPipeline:
    def process_item(self, item, spider):
        return item


class DataBasePipeline(object):
    def __init__(self, db, user, passwd, host, port, table_queries):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port
        self.table_queries = table_queries

    def process_item(self, item: dict, spider):
        if not self.connection:
            return item

        if item.get('badge_url'):
            sql = self._build_query(item)
        else:
            item_title = item['title']
            if item.get('url') in self.articles_urls:
                raise DropItem(
                    f'This article is already in the database: "{item_title}"'
                )
            elif not item.get('body'):
                raise DropItem(
                    f'This article does not have any body: "{item_title}"'
                )

            domain_name = spider.allowed_domains[0]
            domain_query = f"SELECT id FROM domains WHERE domain_name='{domain_name}'"
            self.cursor.execute(domain_query)
            fetched_row = self.cursor.fetchone()
            domain_id = fetched_row[0]

            sql = self._build_query(item, domain_id)

        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except mysql.connector.IntegrityError:
            print('Article already in the DataBase.')
        except Exception as e:
            print(e)
        return item

    def _get_articles_urls(self):
        """Get the stored articles urls from database before scraping."""
        articles_urls_query = "SELECT a.url FROM articles AS a"
        self.cursor.execute(articles_urls_query)
        fetched_rows = self.cursor.fetchall()

        articles_urls = []
        for fetched_row in fetched_rows:
            articles_urls.append(fetched_row[0])

        return articles_urls

    def _build_query(self, item: dict, domain_id: int = None) -> str:
        """Build a query to save scraped items into the MySQL database."""
        if not domain_id:
            self.cursor.execute(self.table_queries['courses'])

            course_insert_query = """
                INSERT INTO courses(
                    title,
                    badge_url,
                    url,
                    overview
                )
                VALUES (
                    '{title}',
                    '{badge_url}',
                    '{url}',
                    '{overview}'
                )"""
            course_insert_query = course_insert_query.format(**item)

            return course_insert_query
        else:
            self.cursor.execute(self.table_queries['articles'])

            article_insert_query = """
                INSERT INTO articles(
                    id_domain,
                    title,
                    overview,
                    url,
                    image_url,
                    body,
                    pub_date
                )
                VALUES (
                    '{domain_id}',
                    '{title}',
                    '{overview}',
                    '{url}',
                    '{image_url}',
                    '{body}',
                    '{pub_date}'
                )"""
            article_insert_query = article_insert_query.format(**item, domain_id=domain_id)

            return article_insert_query

    def open_spider(self, spider):
        try:
            self.connection = mysql.connector.connect(
                    db=self.db,
                    user=self.user,
                    host=self.host,
                    passwd=self.passwd,
                    charset='utf8mb4',
                    use_unicode=True,
                    port=self.port,
                    auth_plugin='mysql_native_password'
                )
            self.cursor = self.connection.cursor()
            self.articles_urls = self._get_articles_urls()
            print('Succesful Connection')
        except Error as err:
            print('There was an error trying to connect to the database: {err}'.format(err))

    def close_spider(self, spider):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    @classmethod
    def from_crawler(cls, crawler):
        table_queries = crawler.settings.getdict('TABLE_QUERIES')
        db_settings = crawler.settings.getdict('DB_SETTINGS')
        if not db_settings:
            raise NotConfigured(
                'Make sure you are exporting the DataBase env variables.'
            )
        return cls(**db_settings, table_queries=table_queries)

