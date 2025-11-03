#!/bin/bash

# Emergent AI Compliance - Docker Quick Start Script
# This script sets up and starts the entire application with Docker

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Emergent AI Compliance - Docker Setup                  ║"
echo "║   EU AI Act Compliance Analysis Tool                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first:"
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✓ Docker is installed"
echo "✓ Docker Compose is installed"
echo ""

# Stop any existing services
echo "Stopping any existing services..."
docker-compose down 2>/dev/null || true
echo ""

# Build images
echo "Building Docker images..."
echo "This may take a few minutes on first run..."
docker-compose build --progress=plain
echo ""

# Start services
echo "Starting services..."
docker-compose up -d
echo ""

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 5

# Check MongoDB
echo -n "Checking MongoDB... "
for i in {1..30}; do
    if docker exec emergent-compliance-mongodb mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; then
        echo "✓"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Failed to connect to MongoDB"
        exit 1
    fi
    sleep 2
done

# Check Backend
echo -n "Checking Backend API... "
for i in {1..30}; do
    if curl -f http://localhost:8001/api/ > /dev/null 2>&1; then
        echo "✓"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Backend failed to start"
        echo "Check logs with: docker-compose logs backend"
        exit 1
    fi
    sleep 2
done

# Check Frontend
echo -n "Checking Frontend... "
for i in {1..30}; do
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        echo "✓"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Frontend failed to start"
        echo "Check logs with: docker-compose logs frontend"
        exit 1
    fi
    sleep 2
done

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   ✓ All services are running!                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Access the application:"
echo "  🌐 Frontend:        http://localhost:3000"
echo "  🔧 Backend API:     http://localhost:8001"
echo "  📚 API Docs:        http://localhost:8001/docs"
echo "  🗄️  MongoDB:         mongodb://localhost:27017"
echo ""
echo "Useful commands:"
echo "  View logs:          docker-compose logs -f"
echo "  Stop services:      docker-compose down"
echo "  Restart:            docker-compose restart"
echo ""
echo "For more commands, see DOCKER.md or run: make help"
echo ""
