# Dogtraining Docker Setup

## 1. Build Docker Images

Build the backend image:

```sh
docker build -t dogtraining:latest -f dogtraining.Dockerfile .
```

Build the frontend image:

```sh
docker build -t client:latest -f client.Dockerfile .
```

## 2. Initialize Database (Only Once)

Initialize the SQLite database before starting the application for the first time:

```sh
python init_database.py --connection=sqlite+aiosqlite:////home/damian-sommer/dev/dogtraining/test.db
```

Make sure the database path matches the path configured in `docker-compose.yml`.

**Important:** Database initialization only needs to be performed once. Do not repeat this step when restarting the application.

## 3. Run Backend and Frontend Individually

You can also run the backend and frontend separately without Docker Compose.

### Backend

```sh
docker run -v $HOME/dev/dogtraining/test.db:/home/test.db -p 5555:50 -it dogtraining:latest python -m dogtraining.server --connection=sqlite+aiosqlite:///home/test.db --frontend_host_url=http://localhost:8888 --port=50 --host=0.0.0.0
```

### Frontend

```sh
docker run -p 8888:80 -e VITE_SERVER_IP=localhost -e VITE_SERVER_BACKEND_PORT=5555 -it client:latest
```

## 4. Run Backend and Frontend with Docker Compose

Alternatively, start both services together using Docker Compose:

```sh
docker compose up -d
```

Access the application:

- Frontend: http://localhost:8888
- Backend: http://localhost:5555

### Managing Docker Compose

View running containers:

```sh
docker compose ps
```

View logs:

```sh
docker compose logs -f
```

View backend logs:

```sh
docker compose logs -f backend
```

View frontend logs:

```sh
docker compose logs -f client
```

Stop both services:

```sh
docker compose down
```

Restart both services:

```sh
docker compose restart
```

## 5. Updating the Application

If you make changes to the backend or frontend code, rebuild the corresponding image:

Rebuild backend:

```sh
docker build -t dogtraining:latest -f dogtraining.Dockerfile .
```

Rebuild frontend:

```sh
docker build -t client:latest -f client.Dockerfile .
```

After rebuilding, recreate the containers:

```sh
docker compose up -d --force-recreate
```

## Important Notes

- Both Docker Compose services communicate through a shared Docker network.
- The SQLite database is mounted into the backend container and persists across container restarts and recreations.
- The backend is accessible on port `5555`, and the frontend on port `8888`.
- Database initialization is a one-time operation and should not be repeated during normal application startup.
- Do not add a trailing slash to the `frontend_host_url` parameter. The CORS configuration expects the exact frontend URL without a trailing slash.
- When running the containers individually, the frontend and backend are not automatically part of a shared Docker network.