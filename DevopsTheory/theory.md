# DevOps Theory Notes

This document summarizes the core theory and practical concepts demonstrated in the DevopsTheory directory.

## 1) Multi-Container Orchestration with Docker Compose

Reference files:
- docker-compose.yml
- compose-tutorial/docker-compose.yml

Concepts covered:
- Defining multiple services in a single YAML file.
- Service-to-service communication over user-defined networks.
- Persistent data using named volumes.
- Environment variable based runtime configuration.
- Port mapping from host to container.
- Startup ordering with depends_on.
- Mapping equivalent docker run flags to Compose fields.

Why it matters:
- Compose turns repeated container run commands into declarative infrastructure.
- It improves reproducibility, readability, and team collaboration.

## 2) Containerizing a Python Application

Reference files:
- ClassPython/app.py
- ClassPython/Dockerfile

Concepts covered:
- Choosing a minimal base image (python:3.10-slim) to reduce image size.
- Defining working directory with WORKDIR.
- Copying application source into image with COPY.
- Installing dependencies during build with RUN pip install.
- Setting container start command using CMD.

Why it matters:
- Demonstrates standard Docker build flow for Python workloads.
- Shows dependency packaging so runtime is independent of host machine setup.

## 3) Containerizing a Java Application

Reference files:
- docker-class/Hello.java
- docker-class/Dockerfile
- docker-class/Second.Dockerfile

Concepts covered:
- Building a Java runtime environment on Ubuntu.
- Installing JDK inside image and compiling source (javac).
- Executing compiled Java application at container startup.
- Understanding ENTRYPOINT and CMD interaction (Second.Dockerfile).

Why it matters:
- Reinforces language-agnostic containerization principles.
- Clarifies startup command design and how container arguments are handled.

## 4) Data and Directory Mapping Concepts

Reference items:
- classdir/
- classdir2/

Concepts covered:
- Host directory usage for persistence and data sharing.
- Relationship between host file system paths and container paths.

Why it matters:
- Persistent and shared data is essential for stateful apps and local development workflows.

## 5) Exported Image Artifact

Reference item:
- java-app.tar

Concepts covered:
- Saving and transporting Docker images as tar archives.
- Offline transfer and portability of pre-built images.

Why it matters:
- Useful in restricted environments and for artifact distribution without direct registry access.

## Summary

The DevopsTheory directory demonstrates foundational container concepts:
- Image creation for multiple languages.
- Runtime configuration and startup behavior.
- Multi-container composition.
- Networking and volume persistence.
- Portability of container artifacts.

Together, these form a practical base for DevOps workflows and production-ready containerized application design.
