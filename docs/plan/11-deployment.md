# Deployment

## Docker Setup

### docker-compose.yml (production)

```yaml
services:
  api:
    build:
      context: .
      dockerfile: services/api/Dockerfile
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/opendesign
      - LLM_BASE_URL=https://api.openai.com/v1
      - LLM_API_KEY=${LLM_API_KEY}
      - LLM_MODEL=gpt-4
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:8080/health"]
      interval: 10s
      timeout: 5s
      retries: 3

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=opendesign
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

### docker-compose.dev.yml (development)

```yaml
services:
  api:
    volumes:
      - ./services/api:/app
      - ./migrations:/migrations
    command: ["go", "run", "./cmd/api", "--addr=:8080"]
    ports:
      - "8080:8080"
```

## Dockerfile (Go Backend)

```dockerfile
# Build stage
FROM golang:1.23-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o api ./cmd/api

# Runtime stage
FROM alpine:3.20
RUN apk --no-cache add ca-certificates
COPY --from=builder /app/api /usr/local/bin/api
EXPOSE 8080
ENTRYPOINT ["api"]
```

## Configuration

All configuration via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `:8080` | HTTP listen address |
| `DATABASE_URL` | required | PostgreSQL connection string |
| `LLM_BASE_URL` | required | OpenAI-compatible API base URL |
| `LLM_API_KEY` | required | API key for LLM provider |
| `LLM_MODEL` | `gpt-4` | Model to use |
| `JWT_SECRET` | required | Secret for JWT signing |
| `UPLOAD_DIR` | `./uploads` | Directory for file uploads |
| `MAX_UPLOAD_SIZE` | `26214400` | Max upload size in bytes (25MB) |

## Production Checklist

- [ ] JWT_SECRET is strong random string
- [ ] LLM_API_KEY is valid
- [ ] DATABASE_URL points to production database
- [ ] Upload directory is writable
- [ ] Reverse proxy (nginx/caddy) terminates TLS
- [ ] Health check endpoint responds
- [ ] Graceful shutdown configured
- [ ] Log output is structured (JSON)
