# FacilComanda Microservices

Migrated Spring Boot microservices workspace for the former `FacilComanda` monolith.

## Requirements

- Java 17
- Maven 3.9+
- Docker
- Docker Compose

## Build

```bash
mvn clean install
```

## Run Infrastructure

```bash
docker compose up -d rabbitmq postgres discovery-server config-server api-gateway
```

PostgreSQL initialization creates one database per data-owning service using `docker/postgres/init/01-create-databases.sql`.

## Run All Services

```bash
docker compose up --build
```

## Useful URLs

- Eureka Dashboard: http://localhost:8761
- RabbitMQ Dashboard: http://localhost:15672
- API Gateway: http://localhost:8080
- Auth Swagger: http://localhost:8081/swagger-ui.html
- User Swagger: http://localhost:8082/swagger-ui.html
- Category Swagger: http://localhost:8083/swagger-ui.html
- Product Swagger: http://localhost:8084/swagger-ui.html
- Restaurant Swagger: http://localhost:8085/swagger-ui.html
- Table Swagger: http://localhost:8086/swagger-ui.html
- Order Swagger: http://localhost:8087/swagger-ui.html
- Audit Swagger: http://localhost:8088/swagger-ui.html
- Actuator health: `/actuator/health` on every service

## Environment Variables

- `CONFIG_SERVER_URL`
- `EUREKA_DEFAULT_ZONE`
- `DB_URL`
- `DB_USER`
- `DB_PASSWORD`
- `DB_DDL_AUTO`
- `RABBITMQ_HOST`
- `RABBITMQ_PORT`
- `RABBITMQ_USER`
- `RABBITMQ_PASSWORD`
- `JWT_SECRET`
- `JWT_EXPIRATION`

## Gateway Routes

- `/api/auth/**` -> auth-service
- `/api/users/**`, `/api/roles/**` -> user-service
- `/api/categories/**` -> category-service
- `/api/products/**` -> product-service
- `/api/organizations/**`, `/api/restaurant-floors/**` -> restaurant-service
- `/api/tables/**` -> table-service
- `/api/orders/**` -> order-service
- `/api/audit/**` -> audit-service
