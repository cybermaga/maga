# 🚀 GitHub Setup - Быстрый старт

## Шаг 1: Создайте репозиторий на GitHub

1. Зайдите на https://github.com
2. Нажмите **"New repository"** (зеленая кнопка)
3. Заполните:
   - **Repository name**: `emergent-ai-compliance`
   - **Description**: "EU AI Act Compliance Analysis Tool - SDK and Web Application"
   - **Visibility**: Public или Private (на ваш выбор)
   - ⚠️ **НЕ ставьте галочки** на "Initialize with README", "Add .gitignore", "Choose a license"
4. Нажмите **"Create repository"**

---

## Шаг 2: Подключите проект к GitHub (в Emergent)

В терминале Emergent выполните:

```bash
cd /app

# Инициализация git (если еще не сделано)
git init

# Добавить все файлы
git add .

# Создать первый коммит
git commit -m "Initial commit: EU AI Act Compliance SDK & Application"

# Подключить к вашему GitHub репозиторию
# Замените YOUR_USERNAME и YOUR_REPO на ваши данные
git remote add origin https://github.com/YOUR_USERNAME/emergent-ai-compliance.git

# Отправить код на GitHub
git branch -M main
git push -u origin main
```

### Если нужна аутентификация:

**Вариант 1: Personal Access Token (рекомендуется)**

1. Зайдите на GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Нажмите "Generate new token (classic)"
3. Выберите scopes: `repo` (полный доступ к репозиториям)
4. Скопируйте токен
5. При push используйте токен вместо пароля:
```bash
git push -u origin main
# Username: ваш_username
# Password: вставьте_токен
```

**Вариант 2: SSH ключ**

```bash
# Сгенерировать SSH ключ
ssh-keygen -t ed25519 -C "your_email@example.com"

# Показать публичный ключ
cat ~/.ssh/id_ed25519.pub

# Скопируйте ключ и добавьте на GitHub:
# GitHub → Settings → SSH and GPG keys → New SSH key

# Используйте SSH URL
git remote set-url origin git@github.com:YOUR_USERNAME/emergent-ai-compliance.git
git push -u origin main
```

---

## Шаг 3: Клонируйте на свой компьютер

Теперь вы можете клонировать проект на любой компьютер:

```bash
# HTTPS
git clone https://github.com/YOUR_USERNAME/emergent-ai-compliance.git

# или SSH
git clone git@github.com:YOUR_USERNAME/emergent-ai-compliance.git

cd emergent-ai-compliance
```

---

## Шаг 4: Запустите проект с Docker

### На вашем компьютере:

1. **Установите Docker Desktop** (если еще не установлен):
   - Windows/Mac: https://www.docker.com/products/docker-desktop
   - Linux:
   ```bash
   curl -fsSL https://get.docker.com | sh
   sudo usermod -aG docker $USER
   # Перелогиньтесь после этого
   ```

2. **Создайте .env файлы** (скопируйте из примеров):
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

3. **Запустите приложение**:
   ```bash
   # Простой способ
   docker-compose up -d

   # Или с помощью Makefile
   make setup

   # Или автоматический скрипт
   chmod +x docker-start.sh
   ./docker-start.sh
   ```

4. **Откройте в браузере**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8001
   - API Docs: http://localhost:8001/docs

---

## Шаг 5: Проверка работы

```bash
# Проверить статус контейнеров
docker-compose ps

# Просмотр логов
docker-compose logs -f

# Тест API
curl http://localhost:8001/api/

# Тест frontend
curl http://localhost:3000
```

---

## 🎯 Готово!

Теперь у вас:
✅ Код на GitHub
✅ Приложение запущено локально в Docker
✅ Можно клонировать на любой компьютер

---

## Дополнительные команды Git

```bash
# Посмотреть статус
git status

# Добавить изменения
git add .

# Создать коммит
git commit -m "Описание изменений"

# Отправить на GitHub
git push

# Получить изменения с GitHub
git pull

# Посмотреть историю
git log --oneline

# Создать новую ветку
git checkout -b feature/new-feature

# Переключиться на main
git checkout main
```

---

## Обновление проекта

После изменений в коде:

```bash
# 1. Сохранить изменения
git add .
git commit -m "Update: описание изменений"
git push

# 2. На другом компьютере получить обновления
git pull

# 3. Пересобрать Docker контейнеры
docker-compose down
docker-compose build
docker-compose up -d
```

---

## Структура проекта на GitHub

После push ваш репозиторий будет содержать:

```
emergent-ai-compliance/
├── README.md                    # Основная документация
├── DOCKER.md                    # Docker инструкции
├── DOCKER_QUICK.md              # Быстрый справочник
├── EXAMPLES.md                  # Примеры использования
├── docker-compose.yml           # Development окружение
├── docker-compose.prod.yml      # Production окружение
├── docker-start.sh              # Скрипт запуска
├── Makefile                     # Make команды
├── .gitignore                   # Игнорируемые файлы
├── backend/
│   ├── Dockerfile
│   ├── .env.example            # ← Пример конфига
│   ├── requirements.txt
│   ├── server.py
│   ├── cli.py
│   └── sdk/
├── frontend/
│   ├── Dockerfile
│   ├── .env.example            # ← Пример конфига
│   ├── package.json
│   ├── nginx.conf
│   └── src/
└── nginx/
    └── nginx.conf
```

---

## 🔒 Безопасность

⚠️ **ВАЖНО**: 
- Файлы `.env` уже в `.gitignore` и НЕ попадут на GitHub
- Для примеров используйте `.env.example`
- Никогда не коммитьте реальные пароли и API ключи!

---

## 📚 Полезные ссылки

- [GitHub Documentation](https://docs.github.com)
- [Docker Documentation](https://docs.docker.com)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)

---

## Нужна помощь?

См. также:
- [README.md](README.md) - основная документация
- [DOCKER.md](DOCKER.md) - подробное руководство Docker
- [EXAMPLES.md](EXAMPLES.md) - примеры использования API и SDK
