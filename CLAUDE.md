# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the server
python server.py

# Run with uvicorn directly
uvicorn server:app --reload

# Install dependencies (uses uv)
uv sync
```

Environment variables are loaded from `.env`. Required vars: `environment`, `mongodb_url`, `mongodb_user`, `mongodb_password`, `mongodb_db`, `app_name`, `port`, `host`, `reload`. The `environment` var controls which dependency implementations are injected (`test` vs `dev`/`stage`/`prod`).

## Architecture

This is a **FastAPI + MongoDB** restaurant management backend using **Domain-Driven Design (DDD)** and a **CQRS-like** pattern.

### Layer structure

```
app/
├── application/aggregate/<aggregate>/{commands,queries}/<operation>/
│   └── handler.py, request.py, response.py, __init__.py
├── domain/
│   ├── aggregate/<aggregate>/   # Domain models, value objects, enums
│   ├── repositories/            # Abstract repository interfaces
│   ├── services/                # Abstract service interfaces
│   └── exceptions/              # BaseDomainException subclasses
└── infrastructure/
    ├── persistance/mongodb/
    │   ├── clients/             # MongoClientImpl, MongoTestClient
    │   ├── dao/                 # MongoDB document DTOs
    │   ├── mappers/             # Domain ↔ DAO conversion
    │   └── *_repository.py      # Repository implementations
    └── services/                # EncryptionServiceImpl, EmailServiceImpl, etc.
```

Each operation (e.g., `create_admin`, `login`, `list_admins`) lives in its own folder under `application/aggregate/<aggregate>/{commands,queries}/` and follows the pattern: `Request` → `Handler.handle()` → `Response`.

### Dependency injection

`dependencies.py` contains a `DependencyContainer` IoC container that auto-wires constructor dependencies by type hint. Singletons are registered once; factories are called per-request. The container is environment-aware — `MongoTestClient` and test service stubs are injected when `environment=test`.

Handlers receive repositories and services via constructor injection. Route handlers inject the `Meta` object (user_id, session_id, role, group, jwt) via `Depends(get_session_meta)`.

### MongoDB persistence

Collections: `users`, `sessions`, `verifications`, `dishes`, `tables`, `orders`, `groups`, `indexes`.

Documents use a composite key pattern — `pk` (e.g., `"USER#<uuid>"`) and `sk` (e.g., `"PROFILE#"`) — similar to a DynamoDB single-table design. A separate `indexes` collection maps secondary lookups (e.g., email → user_id) for fast retrieval.

Indexes are created on startup in `ensure_indexes()` inside `server.py`.

### Error handling

`ErrorMiddleWare` catches `BaseDomainException` subclasses and maps them to HTTP status codes. Add new domain errors as subclasses of `BaseDomainException` in `app/domain/exceptions/`.

### Domain aggregates

- **User** — roles: `SUPERADMIN`, `ADMIN`, `WAITER`; group-scoped
- **Session** — JWT-based auth with 1-day TTL
- **Order** — states: Open → In-Process → Ready → Paying → Paid/Cancelled
- **Dish** — states: Available, Unavailable, Out-of-Stock
- **Table** — Active/Inactive
- **Group** — multi-tenancy container

### Adding a new operation

1. Create folder `app/application/aggregate/<aggregate>/{commands|queries}/<operation>/`
2. Add `request.py` (Pydantic model), `response.py`, `handler.py`, `__init__.py`
3. Register the handler in `dependencies.py`
4. Add the route in the aggregate's router file under `app/infrastructure/`
