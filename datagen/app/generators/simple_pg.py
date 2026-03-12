import random
from datetime import datetime, timedelta
from app.models import Install, Action

def generate_installs_and_actions_batch(cfg, batch_size: int = 10):
    """
    Генерирует пачку установок и действий (без задержек).
    Возвращает (list[Install], list[Action])
    """
    installs = []
    actions = []
    now = datetime.now()

    for _ in range(batch_size):
        user_id = str(random.randint(1, 10**6))

        source = random.choice(['banner', 'organic'])
        install_time = now - timedelta(days=random.randint(0, 7),
                                       hours=random.randint(0, 23),
                                       minutes=random.randint(0, 59))
        installs.append(Install(user_id, install_time, source))

        # Регистрация
        reg_time = install_time + timedelta(minutes=random.randint(1, 60))
        actions.append(Action(user_id, reg_time, 'registration'))

        # Первый заказ (60%)
        if random.random() < 0.6:
            order_time = reg_time + timedelta(hours=random.randint(1, 72))
            actions.append(Action(user_id, order_time, 'first_order'))

        # Смена тарифа (30%)
        if random.random() < 0.3:
            switch_time = reg_time + timedelta(days=random.randint(3, 14))
            actions.append(Action(user_id, switch_time, 'tariff_switch'))

    return installs, actions
