# Makefile для управления коннекторами Kafka Connect

# Переменные
CONNECT_HOST = localhost:8083
CONNECTOR_DIR = kafka/connectors_settings
CURL = curl -s -w "\n" -H "Content-Type: application/json"

# Цели
.PHONY: help add remove reset list status

help:
	@echo "Доступные команды:"
	@echo "  make add      - добавить все коннекторы из $(CONNECTOR_DIR)"
	@echo "  make remove   - удалить все активные коннекторы"
	@echo "  make reset    - удалить все и заново добавить"
	@echo "  make list     - показать список имён коннекторов"
	@echo "  make status   - показать детальный статус всех коннекторов"

# Добавить один коннектор из файла
define add_connector
	@echo "➡️  Добавление $(notdir $(1)) ..."
	@$(CURL) -X POST $(CONNECT_HOST)/connectors -d @$(1) | jq '.'
endef

# Удалить один коннектор по имени
define remove_connector
	@echo "❌ Удаление $(1) ..."
	@$(CURL) -X DELETE $(CONNECT_HOST)/connectors/$(1)
endef

# Добавить все коннекторы из папки
add: $(wildcard $(CONNECTOR_DIR)/*.json)
	@if [ -z "$^" ]; then \
		echo "Нет файлов конфигурации в $(CONNECTOR_DIR)"; \
		exit 1; \
	fi
	@for file in $^; do \
		$(call add_connector,$$file); \
	done

# Удалить все коннекторы (получаем список через API)
remove:
	@names=$$($(CURL) $(CONNECT_HOST)/connectors | jq -r '.[]'); \
	if [ -z "$$names" ]; then \
		echo "Нет активных коннекторов"; \
	else \
		for name in $$names; do \
			$(call remove_connector,$$name); \
		done \
	fi

# Сбросить: удалить все и добавить заново
reset: remove add

# Список имён коннекторов
list:
	@$(CURL) $(CONNECT_HOST)/connectors | jq '.'

# Детальный статус всех коннекторов
status:
	@$(CURL) $(CONNECT_HOST)/connectors | jq -r '.[]' | while read name; do \
		echo "=== $$name ==="; \
		$(CURL) $(CONNECT_HOST)/connectors/$$name/status | jq '.connector.state, .tasks[].state'; \
	done
