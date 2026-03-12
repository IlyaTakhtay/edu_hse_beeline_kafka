import logging
import time
import random
from app.config import Config
from app.db.clickhouse import ClickHouseClient
from app.db.postgres import PostgresClient
from app.generators.simple_clickhouse import generate_banner_batch
from app.generators.simple_pg import generate_installs_and_actions_batch

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    cfg = Config()

    ch_client = None
    pg_client = None

    # ClickHouse
    ch_client = ClickHouseClient(cfg)
    ch_client.create_tables()

    # PostgreSQL
    pg_client = PostgresClient(cfg)
    pg_client.create_tables()

    logger.info("Непрерывная генерация данных запущена. Для остановки нажмите Ctrl+C")

    iteration = 0
    try:
        while True:
            iteration += 1

            if cfg.BATCH_IS_RANDOM:
                batch_size = random.randint(cfg.BATCH_SIZE_MIN, cfg.BATCH_SIZE_MAX)
            else:
                batch_size = cfg.BATCH_SIZE_FIXED

            if ch_client is not None:
                batch = generate_banner_batch(batch_size, cfg)
                if batch:
                    ch_client.insert_banners(batch)
                    logger.debug(f"Итерация {iteration}: вставлено {len(batch)} баннеров")

            if pg_client is not None:
                installs, actions = generate_installs_and_actions_batch(cfg, batch_size=batch_size)
                if installs:
                    pg_client.insert_installs(installs)
                if actions:
                    pg_client.insert_actions(actions)
                logger.info(f"Итерация {iteration}: вставлено {len(installs)} установок и {len(actions)} действий")

            if cfg.SLEEP_IS_RANDOM:
                sleep_time = random.uniform(cfg.SLEEP_MIN, cfg.SLEEP_MAX)
            else:
                sleep_time = cfg.SLEEP_FIXED

            time.sleep(sleep_time)

    except KeyboardInterrupt:
        logger.info("Остановка генератора по запросу пользователя")

if __name__ == '__main__':
    main()
