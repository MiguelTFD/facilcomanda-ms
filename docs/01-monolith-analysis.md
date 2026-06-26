# 01 - Monolith Analysis

## Current Architecture Summary

The source backend is a Maven Spring Boot monolith (`com.facilcomanda.erp`) using Spring Boot 3.2.5 and Java 17. It exposes REST APIs under `/api/**`, persists data with Spring Data JPA and PostgreSQL, validates request records with Jakarta Validation, and secures requests with a stateless JWT filter.

The application package is organized by technical layer: `controller`, `service`, `repository`, `model`, `model.enums`, `dto`, and `security`.

## Main Dependencies

- Spring Boot Starter Web
- Spring Boot Starter Data JPA
- Spring Boot Starter Security
- Spring Boot Starter Validation
- PostgreSQL driver
- JJWT 0.12.5
- OpenPDF 1.3.30
- Spring Boot Test and Spring Security Test

## Database Configuration

The monolith uses PostgreSQL from `application.yml`, loading optional `.env` values. Hibernate uses `ddl-auto: validate`, `PostgreSQLDialect`, and tenant filtering is implemented with Hibernate filters using `organization_id`.

## Security And Authentication

- `POST /api/auth/login` and `POST /api/auth/register` are public.
- Other `/api/**` routes require authentication.
- JWT contains `organizationId` and `role` claims.
- `AuthenticationFilter` extracts the JWT and creates `CustomAuthentication`.
- `TenantFilterEnabler` enables Hibernate `tenantFilter` based on `organizationId`.
- Passwords use BCrypt.

## Detected Domains

- Auth: login, register, JWT creation and validation.
- User and role management: users, roles, password encoding.
- Organization/restaurant: organizations and floors.
- Table management: restaurant tables and table state.
- Catalog: categories and products.
- Ordering: orders, order items, table occupancy, stock deduction.

## Entities

- `Organization`: restaurant/company owner data.
- `Role`: role per organization.
- `User`: user account tied to role and organization.
- `Category`: product category with optional parent category.
- `Product`: stock, pricing, discount, expiration, many-to-many categories.
- `RestaurantFloor`: floor/area in a restaurant.
- `RestaurantTable`: table with state, chairs, and floor.
- `Order`: idempotent order, status, table, user, total, optimistic version.
- `OrderItem`: ordered product, quantity, subtotal, comments.

## API Endpoints

- `POST /api/auth/login`
- `POST /api/auth/register`
- `POST /api/categories`
- `GET /api/categories`
- `GET /api/categories/{id}`
- `PUT /api/categories/{id}`
- `DELETE /api/categories/{id}`
- `POST /api/products`
- `GET /api/products`
- `GET /api/products/{id}`
- `PUT /api/products/{id}`
- `DELETE /api/products/{id}`
- `POST /api/organizations`
- `GET /api/organizations/my`
- `PUT /api/organizations/my`
- `POST /api/restaurant-floors`
- `GET /api/restaurant-floors`
- `GET /api/restaurant-floors/{id}`
- `PUT /api/restaurant-floors/{id}`
- `DELETE /api/restaurant-floors/{id}`
- `POST /api/roles`
- `GET /api/roles`
- `GET /api/roles/{id}`
- `PUT /api/roles/{id}`
- `DELETE /api/roles/{id}`
- `POST /api/tables`
- `GET /api/tables`
- `GET /api/tables/{id}`
- `PUT /api/tables/{id}`
- `DELETE /api/tables/{id}`
- `GET /api/tables/floor/{floorId}`
- `POST /api/users`
- `GET /api/users`
- `GET /api/users/{id}`
- `PUT /api/users/{id}`
- `DELETE /api/users/{id}`
- `POST /api/orders`
- `GET /api/orders`

## Main Relationships

- `User` belongs to an organization and role.
- `Role` belongs to an organization.
- `Category` belongs to an organization and may have a parent category.
- `Product` belongs to an organization and has many categories.
- `RestaurantTable` belongs to a floor and organization.
- `Order` belongs to an organization, optional table, and user.
- `OrderItem` belongs to an order and product.

## Transaction Boundaries

The main explicit transaction is order creation. It checks idempotency, loads the authenticated user, occupies the selected table, validates and deducts product stock, calculates item subtotals and total, and persists the order with cascading order items.

## Risks And Assumptions

- The monolith enum contains Spanish role names, while organization authorization checks mention `WEB_OWNER` and `ORG_MASTER`; the migration keeps both sets as compatible role values.
- The generated microservices remove cross-service JPA relationships and replace them with IDs and Feign calls.
- Product category names now require category-service availability.
- Order creation is no longer a single local database transaction across products, tables, and orders; it uses synchronous service calls and audit events.
- Hibernate tenant filters were replaced by explicit `organizationId` repository filters per service.
