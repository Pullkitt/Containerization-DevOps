# Assignment 1 Report

## 1. Objective and Scope

This project implements a containerized web application stack with FastAPI and PostgreSQL using Docker Compose and macvlan networking. The implementation focuses on production-style image building, static IP assignment, persistent data storage, and orchestration.

## 2. Technology Stack

- Backend: FastAPI
- Database: PostgreSQL (custom Dockerfile)
- Orchestration: Docker Compose
- Networking: macvlan

## 3. Architecture Design

### Overview

The system is deployed as a two-tier containerized architecture with separated concerns and network isolation via macvlan. The architecture follows container networking best practices by implementing external network configuration, static IP addressing, and service health monitoring.

### Network Configuration

- **External Network**: `container_lan` (driver: macvlan)
- **Subnet**: `172.25.112.0/20` (gateway: `172.25.112.1`)
- **Backend Static IP**: `172.25.115.210`
- **Database Static IP**: `172.25.115.211`
- **Persistence**: Named volume `pulkit-postgres-data` for PostgreSQL data durability

### Service Dependencies and Startup Order

1. Database container starts first and initializes schema via `/docker-entrypoint-initdb.d/01-init.sql`
2. Database healthcheck validates readiness (`pg_isready`)
3. Backend container waits for database to reach healthy state
4. Backend initializes database connection and applies retry logic (30 attempts, 2-second intervals)
5. Backend exposes HTTP endpoint on port 8000 with healthcheck

### Communication Flow

- **Client ↔ Backend**: HTTP REST API (port 8000)
- **Backend ↔ Database**: PostgreSQL protocol (port 5432)
- **Database ↔ Storage**: Local filesystem via Docker named volume

## 4. Functional Implementation

- `POST /records`: inserts a record into PostgreSQL
- `GET /records`: fetches all records
- `GET /health`: confirms API and DB connectivity
- DB connection is fully environment-variable based
- `records` table is auto-created on startup

Example validation payload used:

`{"name":"Pulkit","email":"Pulkit.121477@stu.upes.ac.in"}`

## 5. Docker Image Optimization

### Backend

- Multi-stage build used
- Minimal runtime image (`python:3.12-slim`)
- Non-root runtime user
- Reduced layers and cleaned caches
- `.dockerignore` used

### Database

- Custom Dockerfile based on `postgres:16-alpine`
- Explicit non-root (`postgres`) user
- Initialization SQL through `/docker-entrypoint-initdb.d`

Image size comparison:

| Image | Approach | Size |
| --- | --- | --- |
| container-webapp-backend:latest | multi-stage optimized | 181 MB |
| container-webapp-database:latest | custom Dockerfile | 276 MB |

## 6. Docker Compose Orchestration

- Both services defined in one compose file
- External macvlan network used
- Static IPs assigned
- Named volume for Postgres persistence
- `restart: unless-stopped`
- Healthchecks for backend and database
- `depends_on` with healthy DB condition

## 7. Networking Implementation

### Network Design Diagram

The project uses an external macvlan network for direct IP-layer container isolation and static addressing:

```text
                         WSL2 Host (eth0: 172.25.115.76)
                                     |
                                     | (virtualized/NAT context)
                                     v
    +-----------------------------------------------------------------------+
    | External macvlan network: container_lan                               |
    | Subnet: 172.25.112.0/20   Gateway: 172.25.112.1                       |
    |                                                                       |
    |   +-----------------------------------+       +----------------------+ |
    |   | Backend Container                 |       | Database Container   | |
    |   | Name: pulkit-backend              | ----> | Name: pulkit-postgres| |
    |   | IP: 172.25.115.210                | 5432  | IP: 172.25.115.211   | |
    |   | API Port: 8000                    |       | DB Port: 5432        | |
    |   +------------------^----------------+       +----------------------+ |
    |                      |                                              |
    |                      | HTTP:8000                                     |
    |              +-------+------------------+                           |
    |              | Peer test container/curl |                           |
    |              | Same macvlan network     |                           |
    |              +--------------------------+                           |
    +-----------------------------------------------------------------------+

Note: Host-to-container direct access can fail with macvlan host isolation.
```

### Network Configuration Details

| Component | Value | Purpose |
| --- | --- | --- |
| Network Driver | macvlan | Provides bridge-like container connectivity |
| Network Name | `container_lan` | Compose external network reference |
| Parent Interface | eth0 | WSL2 virtual network interface |
| Subnet | 172.25.112.0/20 | Private RFC1918 address space |
| Gateway | 172.25.112.1 | Network default gateway |
| Backend IP | 172.25.115.210 | Static container address (API endpoint) |
| Database IP | 172.25.115.211 | Static container address (DB endpoint) |
| Usable Range | 172.25.112.0–172.25.127.255 | 4094 addresses available |

### Manual Network Creation Command

```bash
docker network create -d macvlan \
  --subnet=172.25.112.0/20 \
  --gateway=172.25.112.1 \
  -o parent=eth0 \
  container_lan
```

Evidence included:

- Network inspect proof: `sceenshots/docker-inspect.png`
- Static container IP proof: `sceenshots/container-ips.png`

### Macvlan Host Isolation Note

Host-to-container communication can fail by default with macvlan due to host isolation behavior. In WSL2, this is more visible because the network is virtualized. For this reason, API validation was also performed from a peer container on the same macvlan network.

## 8. Persistence Validation

1. Insert records.
2. Restart stack.
3. Fetch records and show data remains.

Evidence included:

- Volume persistence proof: `sceenshots/volume-persistent.png`

## 9. macvlan vs ipvlan Comparison

Provide concise comparison table:

| Criterion | macvlan | ipvlan |
| --- | --- | --- |
| Host isolation behavior | Host cannot always directly access containers without workaround | Usually easier host communication depending on mode |
| Broadcast behavior | More direct Layer-2 style behavior | Reduced Layer-2 complexity in many setups |
| Setup complexity | Simple setup, but host isolation handling is needed | Depends on mode and routing behavior |
| Typical use case | Containers need LAN-like presence with unique virtual MACs | Scale-focused environments that prefer lower MAC overhead |

## 10. Conclusion

The project meets core assignment requirements: separate backend/database Dockerfiles, Compose orchestration, static IP assignment on external macvlan, healthchecks, and named-volume persistence. Future improvements include adding automated tests, centralized logging, and deployment on a native Linux host for direct physical LAN validation.