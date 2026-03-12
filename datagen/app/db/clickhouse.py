from clickhouse_driver import Client
from app.models import BannerEvent

class ClickHouseClient:
    def __init__(self, config):
        self.config = config
        self.client = Client(
            host=config.CLICKHOUSE_HOST,
            port=config.CLICKHOUSE_PORT,
            user=config.CLICKHOUSE_USER,
            password=config.CLICKHOUSE_PASSWORD,
            database=config.CLICKHOUSE_DB
        )

    def create_tables(self):
        self.client.execute('''
            CREATE TABLE IF NOT EXISTS banners (
                banner_id UInt32,
                campaign_id UInt32,
                user_id UInt32,
                timestamp DateTime,
                placement String,
                device_type String,
                os String,
                geo String,
                is_clicked UInt8
            ) ENGINE = MergeTree()
            ORDER BY (timestamp, banner_id)
        ''')

    def insert_banners(self, events: list[BannerEvent]):
        if not events:
            return
        data = [e.as_tuple() for e in events]
        self.client.execute(
            'INSERT INTO banners (banner_id, campaign_id, user_id, timestamp, placement, device_type, os, geo, is_clicked) VALUES',
            data
        )
