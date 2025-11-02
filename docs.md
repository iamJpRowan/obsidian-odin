# Developer Documentation

## Building and Publishing Docker Images

If you made changes to the code and want to publish Docker images:

### Plugin Image

```bash
# Build the plugin image
docker build -f Dockerfile -t yourorg/odin-plugin:latest .

# Tag for versioning
docker tag yourorg/odin-plugin:latest yourorg/odin-plugin:v1.0.0

# Push to registry
docker push yourorg/odin-plugin:latest
docker push yourorg/odin-plugin:v1.0.0
```

### Backend Image

```bash
# Build the backend image
cd packages/backend
docker build -t yourorg/odin-backend:latest .

# Tag for versioning
docker tag yourorg/odin-backend:latest yourorg/odin-backend:v1.0.0

# Push to registry
docker push yourorg/odin-backend:latest
docker push yourorg/odin-backend:v1.0.0
```

### Update docker-compose.yml

After publishing, update the image references in `docker-compose.yml`:

```yaml
services:
  plugin:
    image: yourorg/odin-plugin:latest  # Instead of building locally
    # ...
  backend:
    image: yourorg/odin-backend:latest  # Instead of building locally
    # ...
```

## Local Development

For local development without Docker, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Monorepo Structure

This project uses a monorepo with two packages:

- **packages/plugin/** - Obsidian plugin (TypeScript/React)
- **packages/backend/** - BOR Backend (Python/FastAPI)

Both packages have their own build processes but are orchestrated together via Docker Compose.
