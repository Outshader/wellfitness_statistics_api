# Status API - FastAPI Docker Container

Simple FastAPI server that serves a `/status` endpoint for your gethomepage failure alert widget.

## Quick Start

### Option 1: Using Docker Compose (Easiest)

```bash
docker-compose up -d
```

The API will be available at `http://localhost:8000`

### Option 2: Build and Run Manually

```bash
# Build the image
docker build -t status-api .

# Run the container
docker run -d -p 8000:8000 --name status-api status-api
```

## Endpoints

### GET /status
Returns the current status:
```json
{
  "status": "active",
  "failure": true
}
```

**Example:**
```bash
curl http://localhost:8000/status
```

### POST /status
Update the status. You can update one or both fields:

```bash
# Toggle failure
curl -X POST "http://localhost:8000/status?failure=false"

# Change status
curl -X POST "http://localhost:8000/status?status=inactive"

# Change both
curl -X POST "http://localhost:8000/status?status=inactive&failure=false"
```

### GET /health
Health check:
```json
{"ok": true}
```

## Configuration for gethomepage

In your `services.yaml`:

```yaml
- Services:
    - Failure Alert:
        icon: alert.svg
        href: https://yoursite.com
        widget:
          type: failurealert
          url: http://localhost:8000
```

The widget will query `http://localhost:8000/status` and show "FAILURE" in red when `failure: true`.

## Stopping the Container

```bash
docker-compose down
```

Or if you ran it manually:
```bash
docker stop status-api
docker rm status-api
```

## Logs

```bash
docker-compose logs -f
```

## Customization

Edit `main.py` to change the default values or add more endpoints.

Default values:
```python
status_data = {
    "status": "active",
    "failure": True
}
```

After editing `main.py`, rebuild:
```bash
docker-compose up -d --build
```

## Testing

Open your browser or use curl to test:
- http://localhost:8000/status
- http://localhost:8000/health
