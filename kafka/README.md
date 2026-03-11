# Data Pipeline: PostgreSQL → Kafka → Iceberg

Проект реализует потоковую передачу изменений из PostgreSQL в Apache Iceberg через Debezium и Kafka Connect.

## 🔧 Состав проекта

- **`filebeat/`** – Filebeat для отправки CSV-логов в Kafka.
- **`kafka/`** – Kafka, ZooKeeper, Kafka Connect (Debezium, Iceberg Sink), UI.

### 1. Настройка PostgreSQL

Убедитесь, что PostgreSQL запущен с логической репликацией и пользователь имеет права.

В `docker-compose.yml` для PostgreSQL добавьте:

```yaml
command:
  - postgres
  - -c
  - wal_level=logical
  - -c
  - max_replication_slots=10
  - -c
  - max_wal_senders=10
```

Выполните в БД:
```sql
ALTER USER beeline_user WITH REPLICATION;
```

### 2. Запуск стека Kafka

```bash
cd kafka
docker-compose up -d
```

Проверьте, что плагины Debezium и Iceberg доступны:
```bash
curl http://localhost:8083/connector-plugins | jq
```

### 3. Создание Debezium Source Connector (для таблицы `actions`)

```bash
curl -X POST -H "Content-Type: application/json" --data @connectors_settings/debezium-actions.json http://localhost:8083/connectors
```
### 4. Создание Debezium Source Connector (для таблицы `installs`)

```bash
curl -X POST -H "Content-Type: application/json" --data @connectors_settings/debezium-installs.json http://localhost:8083/connectors
```

#### Управление состоянием (offsets)

Если нужно сбросить позицию коннектора и перечитать целиком таблицу:
```bash
curl -X PUT http://localhost:8083/connectors/debezium-actions/stop
curl -X DELETE http://localhost:8083/connectors/debezium-actions/offsets
curl -X PUT http://localhost:8083/connectors/debezium-actions/resume
```

```bash
curl -X PUT http://localhost:8083/connectors/debezium-installs/stop
curl -X DELETE http://localhost:8083/connectors/debezium-installs/offsets
curl -X PUT http://localhost:8083/connectors/debezium-installs/resume
```

### 4. Установка Iceberg Sink Connector

Скачайте JAR-файл (если ещё не скачан):
```powershell
Invoke-WebRequest -Uri https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-kafka-connect/1.6.0/iceberg-kafka-connect-1.6.0.jar \
  -OutFile connectors\iceberg-kafka-connect-1.6.0.jar
```

Зарегистрируйте коннектор:
```bash
curl -X POST -H "Content-Type: application/json" \
  --data @connectors_settings/iceberg-sink-raw_actions.json \
  http://localhost:8083/connectors
```
