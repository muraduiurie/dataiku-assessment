# DATAIKU ASSESSMENT

## Project Overview

The Dataiku Assessment application consists of two primary components:

**Frontend**: Built using React, providing users with an intuitive and responsive interface for interaction.

**Backend**: Developed using Flask, providing RESTful API services, including a service for fetching the current server time.

The application code structure is clearly organized into two directories:

`app/frontend`: Contains the source code of the React application.

`app/api`: Contains the source code of the Flask backend application.



## Build Automation
Dockerfiles are provided for both the frontend and backend components, streamlining the containerization process. Continuous Integration and Continuous Delivery (CI/CD) processes are automated via GitHub Actions, triggered upon each commit to the main branch.
![img_1.png](images/img_1.png)
This automation pipeline, defined in `.github/workflows/build-and-push.yaml`, builds Docker images and pushes them to a container registry, facilitating consistent deployment.

## Deployment Strategy
Deployment is achieved using Helm charts and automated through ArgoCD, enabling synchronized deployments to a personal Kubernetes cluster. ArgoCD ensures continuous synchronization, keeping the deployed application in its desired state.

![img_3.png](images/img_3.png)

The Helm chart, located in charts/dataiku, provisions the following Kubernetes resources:

- **Frontend Deployment**: Two pods for frontend redundancy and load balancing.
- **API Deployment**: Two pods for backend redundancy and load balancing.
- **Frontend Service**: Load balances traffic across frontend pods.
- **API Service**: Load balances traffic across backend pods.
- **Ingress**: Configures external traffic routing to internal Kubernetes services.
- **ServiceMonitor**: Integrates with Prometheus for detailed application metrics monitoring.

## Kubernetes Cluster Infrastructure
The application contains two pods per component (Api and Frontend) for high availability. The pods are deployed in a Kubernetes cluster, which is managed by ArgoCD. The application is exposed via a service and an ingress controller.

### Architecture Diagram
![img.png](images/img.png)

In order to be able to fully utilize the application, the following components are necessary in the Kubernetes cluster:
- **Ingress Controller**: Manages the ingress resources and routes the traffic to the appropriate service.
- **Cert-Manager**: Manages the TLS certificates for the application and automatically renews them.
- **Prometheus**: Monitors the application and collects metrics from the serviceMonitor resource.
- **Grafana**: Visualizes the metrics collected by Prometheus and provides a dashboard for monitoring the application.
- **ArgoCD**: Manages the deployment of the application and ensures that the application is always in the desired state.

## DNS Configuration
DNS management is configured using the domain registrar IONOS. The application domain, dataiku.promoldova.org, uses a CNAME record pointing to an ingress controller's endpoint, which routes the traffic internally within the Kubernetes cluster.
```
dataiku.promoldova.org. IN CNAME ingress.promoldova.org.
ingress.promoldova.org. IN A 157.245.20.223
```
![img_4.png](images/img_4.png)
## Security via TLS
TLS certificates are managed automatically by Cert-Manager, integrating with Let's Encrypt. Cert-Manager ensures certificates are renewed automatically, maintaining a secure and encrypted communication channel between the clients and the application.
![img_7.png](images/img_7.png)

## Monitoring and Observability
Application monitoring leverages Prometheus and Grafana for real-time observability. Prometheus scrapes metrics exposed by the application's ServiceMonitor resource every 30 seconds, ensuring frequent data updates. Grafana visualizes this data, presenting dashboards with metrics such as request counts, latencies, and performance trends.

The ServiceMonitor definition is available in the Helm chart (`charts/dataiku/templates/service-monitor.yaml`), clearly defining the scraping intervals and endpoints.
![img_5.png](images/img_5.png)