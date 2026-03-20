FROM postgres:16-alpine

LABEL org.opencontainers.image.title="container-webapp-postgres"

COPY init/ /docker-entrypoint-initdb.d/

# Explicitly run as non-root user provided by base image.
USER postgres
