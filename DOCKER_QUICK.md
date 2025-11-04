# 🐳 Docker Quick Reference

## Быстрый старт

```bash
# 1. Запуск всех сервисов
docker-compose up -d

# 2. Проверка статуса
docker-compose ps

# 3. Просмотр логов
docker-compose logs -f

# 4. Остановка сервисов
docker-compose down
```

Приложение доступно по адресу: **http://localhost:3000**

---

## Основные команды

### Управление сервисами

```bash
# Сборка образов
docker-compose build

# Запуск с пересборкой
docker-compose up -d --build

# Перезапуск конкретного сервиса
docker-compose restart backend

# Остановка без удаления
docker-compose stop

# Удаление контейнеров и томов
docker-compose down -v
```

### Просмотр логов

```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb

# Последние 100 строк
docker-compose logs --tail=100 backend
```

### Доступ к контейнерам

```bash
# Backend shell
docker-compose exec backend bash

# MongoDB shell
docker-compose exec mongodb mongosh

# Python в backend
docker-compose exec backend python3

# CLI инструмент
docker-compose exec backend python3 cli.py --help
```

---

## Управление базой данных

### Резервное копирование

```bash
# Создать бэкап
docker exec emergent-compliance-mongodb mongodump \
  --out /data/backup/$(date +%Y%m%d_%H%M%S)

# Скопировать на хост
docker cp emergent-compliance-mongodb:/data/backup ./mongodb-backup
```

### Восстановление

```bash
# Скопировать бэкап в контейнер
docker cp ./mongodb-backup emergent-compliance-mongodb:/data/restore

# Восстановить
docker exec emergent-compliance-mongodb mongorestore /data/restore
```

### Работа с данными

```bash
# Подключиться к MongoDB
docker exec -it emergent-compliance-mongodb mongosh compliance_db

# Просмотр коллекций
show collections

# Просмотр отчетов
db.compliance_scans.find().pretty()

# Количество отчетов
db.compliance_scans.countDocuments()

# Очистка всех отчетов
db.compliance_scans.deleteMany({})
```

---

## Отладка

### Проверка статуса сервисов

```bash
# Список контейнеров
docker-compose ps

# Статус health check
docker inspect --format='{{json .State.Health}}' emergent-compliance-backend | jq

# Использование ресурсов
docker stats
```

### Решение проблем

#### Backend не запускается

```bash
# Проверить логи
docker-compose logs backend

# Пересобрать образ
docker-compose build --no-cache backend
docker-compose up -d backend
```

#### Frontend не загружается

```bash
# Проверить логи
docker-compose logs frontend

# Проверить переменные окружения
docker exec emergent-compliance-frontend env

# Пересобрать
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

#### MongoDB недоступна

```bash
# Проверить статус
docker-compose logs mongodb

# Проверить подключение
docker exec emergent-compliance-mongodb mongosh --eval "db.adminCommand('ping')"

# Перезапустить
docker-compose restart mongodb
```

#### Порт уже занят

```bash
# Найти процесс на порту 8001
sudo lsof -i :8001

# Найти процесс на порту 3000
sudo lsof -i :3000

# Остановить существующие контейнеры
docker-compose down
```

---

## Production deployment

### Создание .env файла

```bash
cat > .env << EOF
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=$(openssl rand -base64 32)
CORS_ORIGINS=https://yourdomain.com
BACKEND_URL=https://api.yourdomain.com
EOF
```

### Запуск production

```bash
# Запуск production compose
docker-compose -f docker-compose.prod.yml up -d

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f

# Остановка
docker-compose -f docker-compose.prod.yml down
```

---

## Makefile команды

Для удобства используйте Makefile:

```bash
make help          # Список всех команд
make setup         # Полная настройка (первый запуск)
make up            # Запуск сервисов
make down          # Остановка сервисов
make restart       # Перезапуск
make logs          # Просмотр всех логов
make logs-backend  # Логи backend
make logs-frontend # Логи frontend
make clean         # Удаление контейнеров и томов
make shell-backend # Shell backend
make shell-db      # MongoDB shell
make health        # Проверка здоровья сервисов
```

---

## Оптимизация

### Очистка Docker

```bash
# Удалить неиспользуемые образы, контейнеры, сети
docker system prune -a

# Удалить всё включая volumes
docker system prune -a --volumes

# Показать использование диска
docker system df
```

### Ограничение ресурсов

Добавьте в `docker-compose.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          memory: 256M
```

---

## Мониторинг

### Логирование

```bash
# Размер логов
docker inspect --format='{{.LogPath}}' emergent-compliance-backend | xargs ls -lh

# Очистка логов
docker-compose down
docker system prune
```

### Метрики

```bash
# Реальное время статистика
docker stats --no-stream

# Конкретный контейнер
docker stats emergent-compliance-backend --no-stream
```

---

## Полезные скрипты

### Автоматический перезапуск при падении

Docker Compose автоматически перезапускает сервисы с `restart: unless-stopped`.

### Healthcheck endpoints

```bash
# Backend health
curl http://localhost:8001/api/

# MongoDB health
docker exec emergent-compliance-mongodb mongosh --eval "db.adminCommand('ping')"
```

---

## Дополнительная информация

- Полная документация: [DOCKER.md](DOCKER.md)
- Примеры использования: [EXAMPLES.md](EXAMPLES.md)
- Основная документация: [README.md](README.md)
