#!/bin/bash

# Winged Application Deployment Script
# This script deploys the entire Winged application to Kubernetes

set -e

echo "🐦 Starting Winged Application Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed or not in PATH"
        exit 1
    fi
    
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
    
    log_info "Prerequisites check passed ✓"
}

# Deploy database first
deploy_database() {
    log_info "Deploying PostgreSQL database..."
    kubectl apply -f k8s/namespace/
    kubectl apply -f k8s/database/
    
    log_info "Waiting for database to be ready..."
    kubectl wait --for=condition=ready pod -l app=postgres-db -n winged --timeout=300s
    
    if [ $? -eq 0 ]; then
        log_info "Database deployed successfully ✓"
    else
        log_error "Database deployment failed"
        exit 1
    fi
}

# Deploy services
deploy_services() {
    log_info "Deploying microservices..."
    kubectl apply -f k8s/services/
    
    log_info "Waiting for services to be ready..."
    sleep 30
    
    log_info "Services deployed successfully ✓"
}

# Deploy backend
deploy_backend() {
    log_info "Deploying backend (BFF)..."
    kubectl apply -f k8s/backend/
    
    log_info "Waiting for backend to be ready..."
    kubectl wait --for=condition=available deployment/backend -n winged --timeout=180s
    
    if [ $? -eq 0 ]; then
        log_info "Backend deployed successfully ✓"
    else
        log_warn "Backend deployment may have issues, check logs"
    fi
}

# Deploy mobile app
deploy_mobile() {
    log_info "Deploying mobile application..."
    kubectl apply -f k8s/mobile/
    
    log_info "Mobile app deployed successfully ✓"
}

# Deploy ingress
deploy_ingress() {
    log_info "Deploying ingress..."
    kubectl apply -f k8s/ingress/
    
    log_info "Ingress deployed successfully ✓"
}

# Show deployment status
show_status() {
    log_info "Deployment Status:"
    echo ""
    kubectl get all -n winged
    echo ""
    
    log_info "Ingress Information:"
    kubectl get ingress -n winged
    echo ""
    
    log_info "Deployment completed! 🎉"
    echo ""
    echo "To access the application:"
    echo "1. Add to /etc/hosts: 127.0.0.1 api.winged.local mobile.winged.local"
    echo "2. Access API: http://api.winged.local"
    echo "3. Access Mobile: http://mobile.winged.local"
    echo ""
    echo "Or use port-forwarding:"
    echo "kubectl port-forward service/backend-service 8000:8000 -n winged"
    echo "kubectl port-forward service/mobile-service 8081:8081 -n winged"
}

# Main deployment flow
main() {
    check_prerequisites
    deploy_database
    deploy_services
    deploy_backend
    deploy_mobile
    deploy_ingress
    show_status
}

# Run deployment
main "$@"