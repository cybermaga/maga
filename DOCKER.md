# Docker Deployment Guide

## Quick Start

### Development Environment

Start all services with Docker Compose:

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs
- **MongoDB**: localhost:27017

---

## Building Individual Services

### Backend

```bash
cd backend
docker build -t emergent-compliance-backend .
docker run -p 8001:8001 \
  -e MONGO_URL=mongodb://mongodb:27017 \
  -e DB_NAME=compliance_db \
  emergent-compliance-backend
```

### Frontend

```bash
cd frontend
docker build -t emergent-compliance-frontend .
docker run -p 3000:80 emergent-compliance-frontend
```

---

## Production Deployment

### Prerequisites

1. Create `.env` file:

```bash
cat > .env << EOF
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=your_secure_password_here
CORS_ORIGINS=https://yourdomain.com
BACKEND_URL=https://api.yourdomain.com
EOF
```

2. Set up SSL certificates (for nginx):

```bash
mkdir -p nginx/ssl
# Place your SSL certificates in nginx/ssl/
# - fullchain.pem
# - privkey.pem
```

### Deploy

```bash
# Build and start production services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Check service health
docker-compose -f docker-compose.prod.yml ps
```

---

## Service Health Checks

All services include health checks:

```bash
# Check all services
docker-compose ps

# Check specific service
docker inspect --format='{{json .State.Health}}' emergent-compliance-backend | jq

# View service logs
docker logs emergent-compliance-backend
docker logs emergent-compliance-frontend
docker logs emergent-compliance-mongodb
```

---

## Monitoring

### View Resource Usage

```bash
# Real-time stats
docker stats

# Service-specific stats
docker stats emergent-compliance-backend emergent-compliance-frontend
```

### Log Management

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs --tail=100 mongodb

# Clear logs
docker-compose down
docker system prune -a
```

---

## Database Management

### Backup MongoDB

```bash
# Create backup
docker exec emergent-compliance-mongodb mongodump \
  --out /data/backup/$(date +%Y%m%d_%H%M%S)

# Copy backup to host
docker cp emergent-compliance-mongodb:/data/backup ./mongodb-backup
```

### Restore MongoDB

```bash
# Copy backup to container
docker cp ./mongodb-backup emergent-compliance-mongodb:/data/restore

# Restore
docker exec emergent-compliance-mongodb mongorestore /data/restore
```

### Access MongoDB Shell

```bash
docker exec -it emergent-compliance-mongodb mongosh

# List databases
show dbs

# Use compliance database
use compliance_db

# View collections
show collections

# Query reports
db.compliance_scans.find().pretty()
```

---

## Scaling

### Scale Backend

```bash
# Run multiple backend instances
docker-compose up -d --scale backend=3

# Add load balancer (nginx)
# Update nginx.conf to distribute load across instances
```

---

## Troubleshooting

### Service won't start

```bash
# Check logs
docker-compose logs backend

# Check if port is already in use
sudo lsof -i :8001
sudo lsof -i :3000

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### MongoDB connection issues

```bash
# Check MongoDB is running
docker-compose ps mongodb

# Check MongoDB logs
docker-compose logs mongodb

# Test connection
docker exec emergent-compliance-mongodb mongosh --eval "db.adminCommand('ping')"
```

### Frontend can't connect to backend

```bash
# Check backend is accessible
curl http://localhost:8001/api/

# Verify environment variables
docker exec emergent-compliance-frontend env | grep REACT_APP

# Rebuild frontend with correct backend URL
docker-compose build frontend
docker-compose up -d frontend
```

### Out of disk space

```bash
# Remove unused containers, images, volumes
docker system prune -a --volumes

# Check disk usage
docker system df
```

---

## Docker Compose Commands Reference

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose stop

# Restart services
docker-compose restart

# View status
docker-compose ps

# View logs
docker-compose logs -f [service]

# Execute command in service
docker-compose exec backend bash

# Rebuild specific service
docker-compose build backend
docker-compose up -d backend

# Scale service
docker-compose up -d --scale backend=3

# Remove all services and volumes
docker-compose down -v
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build images
        run: |
          docker-compose build
      
      - name: Push to registry
        run: |
          docker-compose push
      
      - name: Deploy to server
        run: |
          ssh user@server 'cd /app && docker-compose pull && docker-compose up -d'
```

---

## Security Best Practices

1. **Never commit `.env` files** with sensitive credentials
2. **Use Docker secrets** for production passwords
3. **Regularly update** base images:
   ```bash
   docker-compose pull
   docker-compose up -d
   ```
4. **Scan images** for vulnerabilities:
   ```bash
   docker scan emergent-compliance-backend
   ```
5. **Limit container resources**:
   ```yaml
   services:
     backend:
       deploy:
         resources:
           limits:
             cpus: '1'
             memory: 512M
   ```

---

## Performance Optimization

### Multi-stage builds

Already implemented in Dockerfiles to reduce image size.

### Layer caching

```bash
# Use BuildKit for better caching
DOCKER_BUILDKIT=1 docker-compose build
```

### Volume mounting for development

```yaml
# docker-compose.override.yml
services:
  backend:
    volumes:
      - ./backend:/app
  frontend:
    volumes:
      - ./frontend/src:/app/src
```

---

For more information, see [README.md](README.md)
