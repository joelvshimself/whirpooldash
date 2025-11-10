## Deploy Streamlit on Azure App Service (Web App for Containers)

This guide shows how to containerize and deploy your existing `app.py` (Streamlit) to Azure App Service using Docker.

### Image overview
- Base image: `python:3.11-slim`
- Port: `8080` (container reads `PORT` and defaults to `8080`)
- Binds to `0.0.0.0`
- Non-root runtime user

---

## 1) Build and run locally

From the repository root (`/Users/joel/Documents/progra/whirpooldash`):

```bash
docker build -t your-dockerhub-username/whirpooldash:latest .
```

Run locally (mapping host port 8080 to container 8080):

```bash
docker run --rm -it -p 8080:8080 \
  -e PORT=8080 \
  your-dockerhub-username/whirpooldash:latest
```

Open `http://localhost:8080`.

---

## 2) Push to Docker Hub

Login and push:

```bash
docker login
docker tag your-dockerhub-username/whirpooldash:latest your-dockerhub-username/whirpooldash:latest
docker push your-dockerhub-username/whirpooldash:latest
```

Optionally, push a version tag:

```bash
docker tag your-dockerhub-username/whirpooldash:latest your-dockerhub-username/whirpooldash:v1
docker push your-dockerhub-username/whirpooldash:v1
```

---

## 3) Deploy to Azure App Service (Web App for Containers)

Prereqs:
- Azure CLI installed and logged in: `az login`
- A Resource Group (or create one below)

Create resource group and Linux plan:

```bash
az group create -n rg-whirpooldash -l eastus

az appservice plan create \
  -g rg-whirpooldash \
  -n plan-whirpooldash \
  --is-linux \
  --sku B1
```

Create the Web App using your Docker Hub image:

```bash
az webapp create \
  -g rg-whirpooldash \
  -p plan-whirpooldash \
  -n whirpooldash-web \
  -i your-dockerhub-username/whirpooldash:latest
```

Configure required app settings (ports):

```bash
az webapp config appsettings set \
  -g rg-whirpooldash \
  -n whirpooldash-web \
  --settings WEBSITES_PORT=8080 PORT=8080
```

If your Docker Hub repo is private, set registry credentials:

```bash
az webapp config container set \
  -g rg-whirpooldash \
  -n whirpooldash-web \
  --docker-custom-image-name your-dockerhub-username/whirpooldash:latest \
  --docker-registry-server-url https://index.docker.io \
  --docker-registry-server-user <DOCKERHUB_USERNAME> \
  --docker-registry-server-password <DOCKERHUB_PASSWORD>
```

Browse your app:

```bash
az webapp browse -g rg-whirpooldash -n whirpooldash-web
```

---

## 4) Notes
- The container reads `$PORT` (defaults to 8080). Azure sets `WEBSITES_PORT` and we also set `PORT` explicitly for compatibility.
- `entrypoint.sh` starts Streamlit with `--server.address 0.0.0.0 --server.port $PORT`.
- The Dockerfile installs Python dependencies using a pip cache mount for faster builds and switches to a non-root user for runtime.

---

## 5) GitHub Actions (auto-deploy on main)

A workflow is included at `.github/workflows/deploy.yml`. It:

- Builds and pushes `linux/amd64` image to Docker Hub as `joecast208/whirpooldash:latest` (and `${GITHUB_SHA}`).
- Deploys the container to the Azure Web App `streamlit-app-demos` using a publish profile.
- Triggers on every push to `main` and on manual `workflow_dispatch`.

Required repository secrets:
- `DOCKERHUB_USERNAME`: your Docker Hub username (e.g., `joecast208`)
- `DOCKERHUB_TOKEN`: a Docker Hub access token (from Docker Hub > Account Settings > Security)
- `AZURE_WEBAPP_PUBLISH_PROFILE`: contents of the publish profile from Azure Portal (Web App > Overview > Get publish profile)

After adding the secrets, push to `main` to trigger a build and deploy automatically.


