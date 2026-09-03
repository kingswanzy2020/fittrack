# fittrack

A small Flask workout tracker that exists to be *operated*: it exports custom Prometheus
metrics, ships as a Helm chart, and is built and deployed by a Jenkins pipeline. The app
is deliberately simple so the delivery and monitoring around it can be the interesting
part.

## What's here

| Path | Purpose |
|---|---|
| `app.py` | Flask app with `prometheus-flask-exporter` plus two custom metrics: a `workouts_logged_total` counter labelled by workout type, and an `active_users` gauge |
| `templates/` | Server-rendered dashboard, workouts, and progress pages |
| `Dockerfile` | Container image |
| `Jenkinsfile` | Build → push → deploy pipeline, image tagged with the Jenkins build number |
| `fittrack/` | Helm chart — deployment, service, and a `ServiceMonitor` so Prometheus scrapes it automatically |
| `k8s/` | The same objects as raw manifests, plus a `PrometheusRule` for alerting |
| `monitoring-values.yaml` | Values for the kube-prometheus-stack install |

## Recreating the local environment

Python 3.12:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # versions are already pinned
python app.py                     # http://localhost:5000, metrics at /metrics
```

Container and chart:

```bash
docker build -t fittrack:local .
helm upgrade --install fittrack ./fittrack
```

The Jenkins pipeline expects one credential to exist in Jenkins, `dockerhub-credentials`,
and pushes to the image path set in the `DOCKER_IMAGE` environment variable at the top of
the `Jenkinsfile`. No credentials are stored in this repo.

## Write-up

Full write-up — architecture diagram, pipeline design, dashboards, and results — lives in
my portfolio repo:
**[Projects / kubernetes / helm-cicd-monitoring](https://github.com/kingswanzy2020/Projects/tree/main/kubernetes/helm-cicd-monitoring)**.
