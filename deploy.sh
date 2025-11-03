#!/bin/bash

# Email Intelligence Platform - Production Deployment Script
# This script handles automated deployment to production environment

set -e  # Exit on any error

# Configuration
PROJECT_NAME="email-intelligence"
DOCKER_COMPOSE_FILE="docker-compose.prod.yml"
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Pre-deployment checks
pre_deployment_checks() {
    log_info "Running pre-deployment checks..."

    # Check if Docker is running
    if ! docker info > /dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker first."
        exit 1
    fi

    # Check if docker-compose is available
    if ! command -v docker-compose > /dev/null 2>&1; then
        log_error "docker-compose is not installed."
        exit 1
    fi

    # Check if required files exist
    local required_files=("Dockerfile.prod" "$DOCKER_COMPOSE_FILE" "requirements.txt")
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "Required file missing: $file"
            exit 1
        fi
    done

    # Check if secrets directory exists
    if [[ ! -d "./secrets" ]]; then
        log_warning "Secrets directory not found. Creating..."
        mkdir -p ./secrets
        log_warning "Please ensure secrets are properly configured in ./secrets/"
    fi

    log_success "Pre-deployment checks passed"
}

# Create backup
create_backup() {
    log_info "Creating backup before deployment..."

    mkdir -p "$BACKUP_DIR"

    # Backup database if it exists
    if [[ -f "./data/production.db" ]]; then
        cp "./data/production.db" "$BACKUP_DIR/production_$TIMESTAMP.db"
        log_success "Database backup created: $BACKUP_DIR/production_$TIMESTAMP.db"
    fi

    # Backup configuration files
    if [[ -f "./secrets/secret_key" ]]; then
        cp "./secrets/secret_key" "$BACKUP_DIR/secret_key_$TIMESTAMP"
        log_success "Secret key backup created"
    fi
}

# Build and deploy
deploy() {
    log_info "Starting deployment..."

    # Build the application
    log_info "Building Docker images..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" build --no-cache

    # Stop existing containers gracefully
    log_info "Stopping existing containers..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" down --timeout 30

    # Start new containers
    log_info "Starting new containers..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" up -d

    # Wait for services to be healthy
    log_info "Waiting for services to be healthy..."
    local max_attempts=30
    local attempt=1

    while [[ $attempt -le $max_attempts ]]; do
        if docker-compose -f "$DOCKER_COMPOSE_FILE" ps | grep -q "healthy"; then
            log_success "Services are healthy"
            break
        fi

        log_info "Waiting for services to be healthy... (attempt $attempt/$max_attempts)"
        sleep 10
        ((attempt++))
    done

    if [[ $attempt -gt $max_attempts ]]; then
        log_error "Services failed to become healthy within timeout"
        rollback
        exit 1
    fi
}

# Rollback on failure
rollback() {
    log_warning "Deployment failed. Rolling back..."

    # Stop failed deployment
    docker-compose -f "$DOCKER_COMPOSE_FILE" down

    # Restore from backup if available
    if [[ -f "$BACKUP_DIR/production_$TIMESTAMP.db" ]]; then
        cp "$BACKUP_DIR/production_$TIMESTAMP.db" "./data/production.db"
        log_success "Database restored from backup"
    fi

    log_error "Rollback completed. Please check the logs and try again."
}

# Post-deployment verification
verify_deployment() {
    log_info "Verifying deployment..."

    # Test application health endpoint
    if curl -f -s http://localhost:8000/health > /dev/null; then
        log_success "Application health check passed"
    else
        log_error "Application health check failed"
        return 1
    fi

    # Test nginx proxy
    if curl -f -s http://localhost/health > /dev/null; then
        log_success "Nginx proxy health check passed"
    else
        log_warning "Nginx proxy health check failed (may be expected if SSL-only)"
    fi

    # Check container status
    if docker-compose -f "$DOCKER_COMPOSE_FILE" ps | grep -q "Up"; then
        log_success "All containers are running"
    else
        log_error "Some containers are not running"
        return 1
    fi
}

# Cleanup old backups
cleanup() {
    log_info "Cleaning up old backups..."

    # Keep only last 10 backups
    local backup_count=$(ls -1 "$BACKUP_DIR"/*.db 2>/dev/null | wc -l)
    if [[ $backup_count -gt 10 ]]; then
        ls -1t "$BACKUP_DIR"/*.db | tail -n +11 | xargs rm -f
        log_success "Old backups cleaned up"
    fi
}

# Main deployment process
main() {
    log_info "Starting Email Intelligence Platform deployment"
    log_info "Timestamp: $TIMESTAMP"

    pre_deployment_checks
    create_backup
    deploy

    if verify_deployment; then
        log_success "🎉 Deployment completed successfully!"
        log_info "Application is available at: http://localhost"
        log_info "Grafana dashboard: http://localhost:3000"
        log_info "Prometheus metrics: http://localhost:9090"
    else
        log_error "Deployment verification failed"
        rollback
        exit 1
    fi

    cleanup
}

# Handle command line arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "rollback")
        rollback
        ;;
    "status")
        docker-compose -f "$DOCKER_COMPOSE_FILE" ps
        ;;
    "logs")
        docker-compose -f "$DOCKER_COMPOSE_FILE" logs -f
        ;;
    "stop")
        log_info "Stopping all services..."
        docker-compose -f "$DOCKER_COMPOSE_FILE" down
        log_success "Services stopped"
        ;;
    *)
        echo "Usage: $0 [deploy|rollback|status|logs|stop]"
        echo "  deploy  - Deploy the application (default)"
        echo "  rollback- Rollback to previous version"
        echo "  status  - Show container status"
        echo "  logs    - Show container logs"
        echo "  stop    - Stop all services"
        exit 1
        ;;
esac</content>
</xai:function_call: <parameter name="path">/home/masum/github/EmailIntelligence/deploy.sh
