# 🚀 Kube Traffic Lens App

A lightweight Python Flask application built as a hands-on DevOps and Kubernetes learning project.

The application is designed to demonstrate **containerization, Kubernetes deployments, health checks, traffic management, canary releases, and service-mesh-based traffic splitting**.

---

## 🌟 Features

- 🔢 **Dynamic Application Version**
  - Version is configurable using the `APP_VERSION` environment variable.
  - Useful for identifying different application releases during deployments.

- 🏷️ **Environment Configuration**
  - Supports configurable application name, version, and environment using environment variables.

- 🖥️ **Pod / Hostname Tracking**
  - Displays the hostname of the container/pod handling the request.
  - Useful for observing Kubernetes traffic distribution.

- ❤️ **Liveness Probe**
  - `/health` endpoint for Kubernetes liveness checks.

- 🚦 **Readiness Probe**
  - `/ready` endpoint for Kubernetes readiness checks and traffic routing.

- 🔍 **Application Details**
  - `/api/details` exposes application, version, environment, pod, and hostname information.

- 🐳 **Dockerized Application**
  - Multi-stage Docker build.
  - Lightweight Python runtime image.
  - Runs as a non-root user.

- ⚡ **Production WSGI Server**
  - Uses Gunicorn instead of Flask's development server for containerized deployments.

- ☸️ **Kubernetes Ready**
  - Designed for Kubernetes Deployments, Services, ConfigMaps, health probes, and traffic management.

- 🔄 **Deployment Strategies**
  - Supports learning and experimentation with:
    - Rolling Update
    - Recreate
    - Canary Deployment
    - Blue/Green concepts

- 🎯 **Traffic Splitting**
  - Designed for experimenting with percentage-based traffic routing such as:
    - 90% → v1
    - 10% → v2
  - Header-based routing can also be implemented.

- 🕸️ **Istio Service Mesh**
  - Can be integrated with Istio for advanced traffic management and traffic splitting.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application runtime |
| Flask | Web framework |
| Gunicorn | Production WSGI server |
| HTML / Tailwind CSS | Frontend UI |
| Docker | Containerization |
| Kubernetes | Container orchestration |
| Istio | Service mesh & traffic management |
| Pytest | Application testing |

---

## 📡 Application Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Application UI |
| `/health` | Liveness health check |
| `/ready` | Readiness health check |
| `/api/details` | Application and runtime details |

### Example

```bash
curl http://localhost:8080/health
````

Response:

```json
{
  "status": "UP"
}
```

Check readiness:

```bash
curl http://localhost:8080/ready
```

Response:

```json
{
  "status": "READY",
  "acceptingTraffic": true
}
```

Application details:

```bash
curl http://localhost:8080/api/details
```

---

## 🐳 Docker

Build the image:

```bash
docker build -t kube-traffic-lens-app:v1.0.0 .
```

Run the container:

```bash
docker run -d \
  --name kube-traffic-lens \
  -p 8080:8080 \
  -e APP_VERSION=v1.0.0 \
  -e APP_ENVIRONMENT=docker \
  kube-traffic-lens-app:v1.0.0
```

Check:

```bash
curl http://localhost:8080/api/details
```

---

## 🧪 Testing

Run the test suite:

```bash
python -m pytest -v
```

The project includes tests for:

* Application availability
* Health endpoint
* Readiness endpoint
* Application details
* Environment/version configuration

---

## ☸️ Kubernetes

The application is designed to run as a Kubernetes workload.

Typical architecture:

```text
                    ┌──────────────────┐
                    │      Client      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Ingress / Istio  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     Service      │
                    └────────┬─────────┘
                             │
                   ┌─────────┴─────────┐
                   ▼                   ▼
            ┌──────────────┐    ┌──────────────┐
            │   Pod v1     │    │   Pod v2     │
            │ Application  │    │ Application  │
            └──────────────┘    └──────────────┘
```

### Kubernetes Probes

Liveness:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
```

Readiness:

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
```

---

## 🔄 Deployment Strategies

This project can be used to demonstrate different Kubernetes deployment strategies.

### Rolling Update

```text
v1 → v1/v2 → v2
```

Gradually replaces old pods with new pods.

### Recreate

```text
v1 → terminate v1 → start v2
```

All old pods are terminated before the new version starts.

### Canary

```text
                 ┌── 90% ──> v1
Client ──────────┤
                 └── 10% ──> v2
```

Allows a new application version to receive a controlled percentage of traffic before a complete rollout.

---

## 🕸️ Istio Traffic Management

Istio can be used to control traffic between application versions.

Example:

```text
                    Istio Gateway
                         │
                         ▼
                  VirtualService
                         │
              ┌──────────┴──────────┐
              │                     │
            90%                   10%
              │                     │
              ▼                     ▼
          App v1                  App v2
          Stable                  Canary
```

Traffic can be controlled using:

* Percentage-based routing
* Header-based routing
* Version-based routing
* Canary releases
* Progressive delivery

---

## 🔢 Version Identification

Different versions can be deployed using environment variables.

Example:

```bash
APP_VERSION=v1.0.0
```

or:

```bash
APP_VERSION=v2.0.0
```

The version is exposed through:

```text
/api/details
```

and displayed in the application UI.

This makes it easy to observe which application version is handling traffic during Kubernetes and Istio experiments.

---

## 🏗️ Project Structure

```text
kube-traffic-lens-app/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── pytest.ini
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   └── ...
│
└── tests/
    └── test_app.py
```

---

## 🎯 Learning Objectives

This project is intended as a practical DevOps/Kubernetes lab for learning:

* Python application containerization
* Docker multi-stage builds
* Non-root containers
* Production WSGI deployment
* Kubernetes Deployments
* Kubernetes Services
* ConfigMaps
* Liveness and Readiness Probes
* Rolling Updates
* Recreate Deployments
* Canary Deployments
* Kubernetes traffic distribution
* Istio Service Mesh
* Percentage-based traffic splitting
* Header-based routing
* Progressive Delivery
* Application version tracking
* Pod-level traffic observation
* Automated testing with Pytest

---

## 🚀 Future Enhancements

Planned improvements include:

* [ ] Kubernetes manifests
* [ ] ConfigMap-based configuration
* [ ] Kubernetes Service
* [ ] Ingress
* [ ] Istio Gateway
* [ ] Istio VirtualService
* [ ] Istio DestinationRule
* [ ] Canary traffic splitting
* [ ] Argo Rollouts integration
* [ ] Prometheus metrics
* [ ] Grafana dashboard
* [ ] GitHub Actions CI pipeline
* [ ] Trivy container scanning
* [ ] Image signing with Cosign
* [ ] SBOM generation
* [ ] GitOps deployment with Argo CD

---

## 📚 Project Goal

The goal of **Kube Traffic Lens** is to provide a simple application that makes Kubernetes traffic behavior **visible and easy to understand**.

By displaying the application version and pod hostname, the project makes it possible to visually observe how traffic moves between application versions during:

```text
Docker
  ↓
Kubernetes
  ↓
Deployment
  ↓
Service
  ↓
Ingress
  ↓
Istio
  ↓
Traffic Splitting
  ↓
Canary / Progressive Delivery
```

---

## 👨‍💻 Author

**Kube Traffic Lens App**

Built as a hands-on DevOps and Kubernetes learning project.

---