# Data Pipeline: PostgreSQL → Kafka → Iceberg

Проект реализует потоковую передачу изменений из PostgreSQL в Apache Iceberg через Debezium и Kafka Connect.

## 🔧 Состав проекта

- **`filebeat/`** – Filebeat для отправки CSV-логов в Kafka.
- **`kafka/`** – Kafka, ZooKeeper, Kafka Connect (Debezium, Iceberg Sink), UI.

### 1. Запуск стека Kafka
#### Возможно потребуется использовать VPN

```bash
cd kafka
docker-compose up -d
```

Проверьте, что плагины Debezium и Iceberg доступны:
```bash
curl http://localhost:8083/connector-plugins | jq
```

### 2. Создание Debezium Source Connector в PostgreSQL(для таблицы `actions` и `installs`)

```bash
curl -X POST -H "Content-Type: application/json" --data @connectors_settings/debezium-postgres.json http://localhost:8083/connectors
```

#### Управление состоянием (offsets)

Если нужно сбросить позицию коннектора и перечитать целиком таблицу:

```bash
curl -X PUT http://localhost:8083/connectors/debezium-postgres/stop
curl -X DELETE http://localhost:8083/connectors/debezium-postgres/offsets
curl -X PUT http://localhost:8083/connectors/debezium-postgres/resume
```

### 3. Создание clickhouse-kafka-connect

```shell
Invoke-WebRequest -Uri "https://repo1.maven.org/maven2/com/clickhouse/clickhouse-jdbc/0.9.4/clickhouse-jdbc-0.9.4-all.jar" `
  -OutFile "./connectors/clickhouse-jdbc-0.9.4-all.jar"
```

```bash
curl -X POST -H "Content-Type: application/json" --data @connectors_settings/jdbc-clickhouse-banners.json http://localhost:8083/connectors
```

```bash
curl -X PUT http://localhost:8083/connectors/jdbc-clickhouse-banners/stop
curl -X DELETE http://localhost:8083/connectors/jdbc-clickhouse-banners/offsets
curl -X PUT http://localhost:8083/connectors/jdbc-clickhouse-banners/resume
```

### 4. Установка Iceberg Sink Connector

Зарегистрируйте коннектор:
```bash
curl -X POST -H "Content-Type: application/json" \
  --data @connectors_settings/iceberg-sink-raw_actions.json \
  http://localhost:8083/connectors
```
