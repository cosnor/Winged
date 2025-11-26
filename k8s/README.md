# Winged Kubernetes Deployment

This directory contains Kubernetes manifests for deploying the Winged bird identification application.

## Architecture

The application consists of:
- **Backend (BFF)**: API Gateway on port 8000
- **Users Service**: User management on port 8001
- **Sightings Service**: Bird sightings on port 8002
- **ML Worker**: Machine learning processing on port 8003
- **Maps Service**: Geographic data on port 8004
- **Routes Service**: Route planning on port 8005
- **Achievements Service**: User achievements on port 8006
- **Mobile App**: React Native Expo app on port 8081
- **PostgreSQL with PostGIS**: Database with spatial extensions

## Prerequisites

1. **Kubernetes cluster** (local or cloud)
2. **kubectl** configured to connect to your cluster
3. **NGINX Ingress Controller** installed
4. **Docker images** built and available

## Building Docker Images

First, build all the Docker images:

```bash
# Build all services
docker build -t winged/backend:latest ./backend
docker build -t winged/users:latest ./services/users
docker build -t winged/sightings:latest ./services/sightings
docker build -t winged/ml-worker:latest ./services/ml_worker
docker build -t winged/maps:latest ./services/maps
docker build -t winged/routes:latest ./services/routes
docker build -t winged/achievements:latest ./services/achievements
docker build -t winged/mobile:latest ./mobile
```

## Deployment Options

### Option 1: Deploy Everything at Once

```bash
# Deploy all components using Kustomize
kubectl apply -k k8s/

# Check deployment status
kubectl get all -n winged
```

### Option 2: Step-by-Step Deployment

```bash
# 1. Create namespace
kubectl apply -f k8s/namespace/

# 2. Deploy database first
kubectl apply -f k8s/database/

# 3. Wait for database to be ready
kubectl wait --for=condition=ready pod -l app=postgres-db -n winged --timeout=300s

# 4. Deploy microservices
kubectl apply -f k8s/services/

# 5. Deploy backend (BFF)
kubectl apply -f k8s/backend/

# 6. Deploy mobile app
kubectl apply -f k8s/mobile/

# 7. Deploy ingress
kubectl apply -f k8s/ingress/
```

## Accessing the Application

### Local Development

If running locally, add to your `/etc/hosts`:

```
127.0.0.1 api.winged.local
127.0.0.1 mobile.winged.local
```

Then access:
- **API**: http://api.winged.local
- **Mobile App**: http://mobile.winged.local

### Port Forwarding (Alternative)

```bash
# Access backend directly
kubectl port-forward service/backend-service 8000:8000 -n winged

# Access individual services
kubectl port-forward service/users-service 8001:8001 -n winged
kubectl port-forward service/mobile-service 8081:8081 -n winged

# Access database for debugging
kubectl port-forward service/postgres-service 5432:5432 -n winged
```

## Monitoring and Debugging

### Check Pod Status

```bash
# View all pods
kubectl get pods -n winged

# Get detailed pod information
kubectl describe pod <pod-name> -n winged

# View logs
kubectl logs <pod-name> -n winged -f
```

### Check Services

```bash
# View all services
kubectl get services -n winged

# Test service connectivity
kubectl run test-pod --image=busybox --rm -it -n winged -- sh
# Inside the pod:
# wget -qO- http://backend-service:8000/health
```

### Database Access

```bash
# Connect to PostgreSQL
kubectl exec -it deployment/postgres-db -n winged -- psql -U postgres

# List databases
\l

# Connect to a specific service database
\c winged_users
```

## Scaling

```bash
# Scale services up/down
kubectl scale deployment users --replicas=3 -n winged
kubectl scale deployment backend --replicas=5 -n winged

# Auto-scaling (requires metrics server)
kubectl autoscale deployment backend --cpu-percent=50 --min=2 --max=10 -n winged
```

## Updates

```bash
# Update image tags in kustomization.yaml, then:
kubectl apply -k k8s/

# Or update individual deployments:
kubectl set image deployment/users users=winged/users:v1.1.0 -n winged
```

## Cleanup

```bash
# Remove everything
kubectl delete namespace winged

# Or remove specific components
kubectl delete -k k8s/
```

## Production Considerations

1. **Replace image tags** with specific versions instead of `latest`
2. **Use proper domain names** instead of `.local` domains
3. **Configure TLS/SSL** certificates
4. **Set up proper secrets management** for sensitive data
5. **Configure resource limits** based on your cluster capacity
6. **Set up monitoring** with Prometheus/Grafana
7. **Configure backup strategy** for PostgreSQL data
8. **Implement proper logging** with centralized log collection

## Troubleshooting

### Common Issues

1. **Pods stuck in Pending**: Check resource availability and storage class
2. **ImagePullBackOff**: Ensure Docker images are built and accessible
3. **CrashLoopBackOff**: Check pod logs for application errors
4. **Service connection issues**: Verify service names and ports match

### Health Checks

Each service should implement a `/health` endpoint for proper health checking. If not available, remove the livenessProbe and readinessProbe sections from deployments.

## File Structure

```
k8s/
├── namespace/
│   └── winged-namespace.yaml
├── database/
│   ├── postgres-configmap.yaml
│   ├── postgres-deployment.yaml
│   ├── postgres-pvc.yaml
│   ├── postgres-secret.yaml
│   └── postgres-service.yaml
├── backend/
│   ├── backend-configmap.yaml
│   ├── backend-deployment.yaml
│   └── backend-service.yaml
├── services/
│   ├── achievements.yaml
│   ├── maps.yaml
│   ├── ml-worker.yaml
│   ├── routes.yaml
│   ├── sightings.yaml
│   └── users.yaml
├── mobile/
│   └── mobile-deployment.yaml
├── ingress/
│   └── winged-ingress.yaml
└── kustomization.yaml
```