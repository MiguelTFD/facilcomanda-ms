# 02 - Microservices Boundaries

## Final Service List

- `api-gateway`
- `discovery-server`
- `config-server`
- `shared-common`
- `auth-service`
- `user-service`
- `category-service`
- `product-service`
- `restaurant-service`
- `table-service`
- `order-service`
- `audit-service`

## Responsibilities And Owned Data

| Service | Responsibility | Owned entities |
| --- | --- | --- |
| `auth-service` | Login, registration, JWT issuance | Auth projection of users, roles, organizations |
| `user-service` | User and role CRUD | `User`, `Role` |
| `category-service` | Category CRUD and category lookup | `Category` |
| `product-service` | Product CRUD, category association IDs, stock reservation | `Product` |
| `restaurant-service` | Organization profile and restaurant floors | `Organization`, `RestaurantFloor` |
| `table-service` | Restaurant table CRUD and table state | `RestaurantTable` |
| `order-service` | Order creation/listing, idempotency, total calculation | `Order`, `OrderItem` |
| `audit-service` | Central audit event consumption and querying | `AuditLog` |
| `shared-common` | DTOs, enums, JWT/security utilities, events, Feign/Rabbit config | No business tables |

## API Endpoints Per Service

- `auth-service`: `/api/auth/login`, `/api/auth/register`
- `user-service`: `/api/users/**`, `/api/roles/**`
- `category-service`: `/api/categories/**`
- `product-service`: `/api/products/**`
- `restaurant-service`: `/api/organizations/**`, `/api/restaurant-floors/**`
- `table-service`: `/api/tables/**`
- `order-service`: `/api/orders/**`
- `audit-service`: `/api/audit/**`

## Required Feign Clients

- `product-service` -> `category-service` for validating category IDs and resolving names.
- `table-service` -> `restaurant-service` for validating floors and resolving floor names.
- `order-service` -> `user-service` for resolving authenticated user by email.
- `order-service` -> `table-service` for table occupancy and table details.
- `order-service` -> `product-service` for stock reservation and product snapshots.

## RabbitMQ Events

Exchanges:

- `domain.events.exchange`
- `audit.events.exchange`

Audit queue:

- `audit.queue` bound to `audit.created`

Routing keys planned for domain events:

- `user.created`
- `user.updated`
- `product.created`
- `product.updated`
- `product.deleted`
- `category.created`
- `category.updated`
- `category.deleted`
- `order.created`
- `order.updated`
- `order.paid`
- `order.cancelled`
- `audit.created`

The current implementation publishes audit events for create/update/delete/state-change operations and provides common domain event contracts for further asynchronous consumers.

## Shared Code Candidates

- DTO records from the monolith.
- Enums: `RoleName`, `OrderStatus`, `TableState`.
- JWT generation and validation.
- Custom authentication.
- Security filter chain defaults.
- Global exception handling.
- Correlation ID filter.
- RabbitMQ event contracts and configuration.
- Feign header propagation.

## Database Strategy

Each service is designed to own its tables logically. For local development, Docker Compose provisions a shared PostgreSQL instance with service-specific database URLs. Cross-service JPA relationships were replaced with scalar IDs:

- `Product.categoryIds`
- `RestaurantTable.floorId`
- `Order.restaurantTableId`
- `Order.userId`
- `OrderItem.productId`

This keeps the migration scalable while preserving the external API contracts.
