ALTER USER beeline_user WITH REPLICATION;

-- Создание схемы user_events
CREATE SCHEMA IF NOT EXISTS user_events;

-- Таблица для установок
CREATE TABLE IF NOT EXISTS user_events.installs (
    user_id VARCHAR(50),
    install_timestamp TIMESTAMP,
    source VARCHAR(100),
    processing_date DATE DEFAULT CURRENT_DATE
);

-- Таблица для действий пользователей
CREATE TABLE IF NOT EXISTS user_events.fct_actions (
    user_id VARCHAR(50),
    session_start TIMESTAMP,
    actions TEXT,
    processing_date DATE DEFAULT CURRENT_DATE
);

CREATE INDEX IF NOT EXISTS idx_installs_timestamp ON user_events.installs(install_timestamp);

CREATE INDEX IF NOT EXISTS idx_fct_actions_user_id ON user_events.fct_actions(user_id);
