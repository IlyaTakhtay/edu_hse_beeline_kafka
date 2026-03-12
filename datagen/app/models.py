from dataclasses import dataclass
from datetime import datetime

@dataclass
class BannerEvent:
    banner_id: int
    campaign_id: int
    user_id: int
    timestamp: datetime
    placement: str
    device_type: str
    os: str
    geo: str
    is_clicked: int

    def as_tuple(self):
        return (self.banner_id, self.campaign_id, self.user_id, self.timestamp,
                self.placement, self.device_type, self.os, self.geo, self.is_clicked)


@dataclass
class Install:
    user_id: str
    install_timestamp: datetime
    source: str                  # 'banner' или 'organic'

    def as_tuple(self):
        return (self.user_id, self.install_timestamp, self.source)


@dataclass
class Action:
    user_id: str
    session_start: datetime
    actions: str

    def as_tuple(self):
        return (self.user_id, self.session_start, self.actions)
