import random
from datetime import datetime
from faker import Faker
from app.models import BannerEvent
from app.config import Config

fake = Faker('ru_RU')

def generate_banner_batch(batch_size: int, cfg: Config) -> list[BannerEvent]:
    """Генерирует один батч баннерных показов с текущим временем."""
    events = []
    now = datetime.now()
    banner_ids = list(range(1, cfg.BANNER_COUNT + 1))
    campaign_ids = list(range(1, cfg.CAMPAIGN_COUNT + 1))

    for _ in range(batch_size):
        banner_id = random.choice(banner_ids)
        campaign_id = random.choice(campaign_ids)
        user_id = random.randint(1, 10**6)  # большой пул пользователей
        placement = random.choice(cfg.PLACEMENTS)
        device_type = random.choice(cfg.DEVICE_TYPES)
        os = random.choice(cfg.OS_LIST)
        geo = random.choice(cfg.CITIES + [''] * 5) if random.random() > 0.1 else ''
        is_clicked = 1 if random.random() < cfg.CLICK_PROBABILITY else 0

        events.append(BannerEvent(
            banner_id=banner_id,
            campaign_id=campaign_id,
            user_id=user_id,
            timestamp=now,
            placement=placement,
            device_type=device_type,
            os=os,
            geo=geo,
            is_clicked=is_clicked
        ))
    return events
