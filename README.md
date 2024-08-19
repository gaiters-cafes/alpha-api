## Getting Started

### Prerequisites

- [Podman](https://podman-desktop.io/) or [Docker](https://www.docker.com/)
- [Kubernetes](https://kubernetes.io/)
- [Helm](https://helm.sh/)
- [Poetry](https://python-poetry.org/)
- [Trivy](https://github.com/aquasecurity/trivy)
- [Apache Benchmark](https://httpd.apache.org/docs/current/programs/ab.html)

## Local build + compose

### .config file

- The Python application expects `.config` file within the `alpha-api/app/.config` directory with the following keys.
- The docker-compose expects `.env` file within the root directory with the same values as below.
- Helm install also expects `.env` file within the `alpha-api/chart/avapi-chart/.env` direcory.

```sh
#.config
API_KEY=ALPHA_VANTAGE_API_KEY
LOG_LEVEL=INFO
```


### Building the Container

To build the container image, navigate to the `app` directory and use the following command:

```sh
podman build -t av-api:local -f Containerfile .
```

### Running the Container locally

Make sure you're in the root directory and use the following command:

```sh
podman compose up --build

# You need .env file in the root folder for the compose build to work. This is the same as .config file that the python application requires.
```

### Scanning the image locally

```sh
trivy image av-api:local
```

### Working with the Python codebase

Navigate to the `alpha-api/app` directory.

```sh
# Installing the packages
poetry install --no-root

# Starting the uvicorn server
poetry run uvicorn alpha_api.main:app --host 0.0.0.0 --port 8000

# Running pytest
poetry run pytest -v

# Running pyclean
poetry run pyclean .
```

## Deploying to Kubernetes

We're going to assueme you already have the image stored in some sort of registry online.

Navigate to the `chart/avapi-chart/` directory and make sure you have a `.env` file with the correct keys. You can amend the values.yaml file to add the image repo & tags.

### Install release

```sh
helm install avapi-release .
```

### Load testing HPA

```sh
# Create a test container within the cluster
k run load-test --image=alpine -- sleep 1000

# Add apache benchmark package
apk add apache2-utils

# simulate request
ab -n 10000 -c 1000 http://<ip address>:<port>/

# Watch HPA scale
kubectl get hpa -w
```


## Repository structure

```sh
.
├── LICENSE
├── README.md
├── app
│   ├── Containerfile
│   ├── alpha_api
│   │   ├── __init__.py
│   │   ├── av_client.py
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── main.py
│   ├── entrypoint.sh
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── tests
│       ├── __init__.py
│       └── test_main.py
├── chart
│   └── avapi-chart
│       ├── Chart.yaml
│       ├── charts
│       ├── templates
│       │   ├── _helpers.tpl
│       │   ├── deployment.yaml
│       │   ├── hpa.yaml
│       │   ├── secrets.yaml
│       │   └── service.yaml
│       └── values.yaml
├── docker-compose.yaml
└── infra                       # terraform files for the cluster
```