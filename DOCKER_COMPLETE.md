# 🐳 Docker Deployment - Complete

## Файловая структура Docker

```
/app/
├── docker-compose.yml          # Development environment
├── docker-compose.prod.yml     # Production environment
├── docker-start.sh             # Quick start script
├── Makefile                    # Convenient commands
├── .dockerignore               # Exclude files from Docker context
├── backend/
│   ├── Dockerfile              # Backend Python image
│   ├── .dockerignore
│   └── requirements.txt
├── frontend/
│   ├── Dockerfile              # Frontend React image (multi-stage)
│   ├── nginx.conf              # Nginx config for serving React
│   ├── .dockerignore
│   └── .env.docker
└── nginx/
    └── nginx.conf              # Production reverse proxy config
```

---

## Созданные Docker файлы

### 1. **Backend Dockerfile** (`/app/backend/Dockerfile`)
- Базовый образ: Python 3.11-slim
- Устанавливает системные зависимости для WeasyPrint (PDF generation)
- Копирует и устанавливает Python зависимости
- Запускает FastAPI через Uvicorn на порту 8001

### 2. **Frontend Dockerfile** (`/app/frontend/Dockerfile`)
- Multi-stage build для оптимизации размера
- **Build stage**: Node.js 18 Alpine
  - Устанавливает зависимости
  - Собирает production build React приложения
- **Production stage**: Nginx Alpine
  - Копирует собранные файлы из build stage
  - Настраивает Nginx для SPA маршрутизации
  - Порт 80

### 3. **docker-compose.yml** - Development
Включает три сервиса:
- **mongodb**: MongoDB 7.0 с volume для персистентности
- **backend**: FastAPI с healthcheck
- **frontend**: React + Nginx с зависимостью от backend

### 4. **docker-compose.prod.yml** - Production
Дополнительно включает:
- Аутентификацию MongoDB
- Nginx reverse proxy для SSL терминации
- Log rotation
- Resource limits (опционально)

---

## Быстрый запуск

### Вариант 1: Автоматический скрипт

```bash
chmod +x docker-start.sh
./docker-start.sh
```

### Вариант 2: Docker Compose

```bash
docker-compose up -d
```

### Вариант 3: Makefile

```bash
make setup
```

---

## Доступ к приложению

После запуска:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs
- **MongoDB**: mongodb://localhost:27017

---

## Основные команды

```bash
# Просмотр статуса
docker-compose ps

# Логи
docker-compose logs -f
docker-compose logs -f backend

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Доступ к shell
docker-compose exec backend bash
docker-compose exec mongodb mongosh

# Полная очистка
docker-compose down -v
```

---

## Production развертывание

### 1. Подготовка

Создайте `.env` файл:

```bash
cat > .env << EOF
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=your_secure_password_here
CORS_ORIGINS=https://yourdomain.com
BACKEND_URL=https://api.yourdomain.com
EOF
```

### 2. SSL сертификаты

```bash
mkdir -p nginx/ssl
# Поместите ваши сертификаты:
# - nginx/ssl/fullchain.pem
# - nginx/ssl/privkey.pem
```

### 3. Запуск

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 4. Проверка

```bash
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f
```

---

## Преимущества Docker версии

✅ **Изоляция**: Все зависимости изолированы в контейнерах
✅ **Портативность**: Работает одинаково на любой системе с Docker
✅ **Простота**: Один команда для запуска всего стека
✅ **Масштабируемость**: Легко масштабировать сервисы
✅ **Консистентность**: Development = Production окружение
✅ **Быстрое развертывание**: От нуля до работающего приложения за минуты

---

## Размеры образов (примерно)

- **Backend**: ~400-500 MB (Python + dependencies)
- **Frontend**: ~25-30 MB (multi-stage build, только production artifacts)
- **MongoDB**: ~700 MB (официальный образ)

---

## Healthchecks

Все сервисы имеют встроенные healthchecks:

### Backend
```bash
curl -f http://localhost:8001/api/
```

### Frontend
```bash
curl -f http://localhost:3000
```

### MongoDB
```bash
docker exec mongodb mongosh --eval "db.adminCommand('ping')"
```

---

## Monitoring и Logs

### Просмотр логов в реальном времени

```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f backend
```

### Проверка использования ресурсов

```bash
docker stats
```

### Очистка логов

```bash
docker-compose down
docker system prune
```

---

## Backup и Restore

### MongoDB Backup

```bash
# Создать backup
docker exec mongodb mongodump --out /data/backup/$(date +%Y%m%d)

# Скопировать на хост
docker cp mongodb:/data/backup ./mongodb-backup
```

### MongoDB Restore

```bash
# Скопировать в контейнер
docker cp ./mongodb-backup mongodb:/data/restore

# Восстановить
docker exec mongodb mongorestore /data/restore
```

---

## Troubleshooting

### Порт уже занят

```bash
sudo lsof -i :8001  # Backend
sudo lsof -i :3000  # Frontend
sudo lsof -i :27017 # MongoDB
```

### Пересборка образов

```bash
docker-compose build --no-cache
docker-compose up -d
```

### Очистка всего

```bash
docker-compose down -v --rmi all
docker system prune -a --volumes
```

---

## CI/CD Integration

### GitHub Actions пример

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build and push
        run: |
          docker-compose build
          docker-compose push
      
      - name: Deploy to server
        run: |
          ssh user@server 'cd /app && docker-compose pull && docker-compose up -d'
```

---

## Дополнительные материалы

- [DOCKER.md](DOCKER.md) - Полная документация
- [DOCKER_QUICK.md](DOCKER_QUICK.md) - Быстрый справочник
- [README.md](README.md) - Основная документация проекта
- [EXAMPLES.md](EXAMPLES.md) - Примеры использования

---

## Итог

Docker версия готова к использованию! Все необходимые файлы созданы и настроены. 

Для запуска достаточно выполнить:

```bash
docker-compose up -d
```

И приложение будет доступно по адресу http://localhost:3000
