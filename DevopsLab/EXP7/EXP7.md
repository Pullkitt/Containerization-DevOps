# Lab - Experiment 7

## CI/CD using Jenkins, GitHub and Docker Hub

**Name:** Pulkit Jain  
**SAP ID:** 500121477  
**Batch:** B3 (CCVT)

---

## 1. Aim

To design and implement a complete CI/CD pipeline using Jenkins, integrating source code from GitHub, and building and pushing Docker images to Docker Hub.

---

## 2. Objectives

- Understand the CI/CD workflow using Jenkins as a GUI-based automation tool
- Create a structured GitHub repository with application code and a Jenkinsfile
- Build Docker images from source code
- Securely store Docker Hub credentials in Jenkins
- Automate build and push operations using webhook triggers
- Use the same host Docker engine as the Jenkins agent

---

## 3. Theory

### 3.1 What is Jenkins?

Jenkins is a web-based automation server used to:

- Build applications
- Test code
- Deploy software

It provides:

- A browser-based dashboard
- A plugin ecosystem for GitHub, Docker, and many other tools
- Pipeline as Code through a Jenkinsfile

### 3.2 What is CI/CD?

**Continuous Integration (CI):**

- Code is automatically built and tested after every commit

**Continuous Deployment or Delivery (CD):**

- Built artifacts are automatically delivered or deployed

### 3.3 Workflow Overview

Developer -> GitHub -> Webhook -> Jenkins -> Build -> Docker Hub

---

## 4. Prerequisites

- Docker and Docker Compose installed
- GitHub account
- Docker Hub account
- Basic Linux command knowledge

---

## 5. Part A: GitHub Repository Setup (Source Code + Build Definition)

### 5.1 Create Repository

Create a GitHub repository named `my-app`.

This repository should contain both the application source code and the pipeline definition so that the entire build process can be version controlled.

### 5.2 Project Structure

```text
my-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
```

### 5.3 Application Code

#### app.py

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello from CI/CD Pipeline!"
    # return "Hello from CI/CD Pipeline!, my sapid is 123456"


app.run(host="0.0.0.0", port=80)
```

#### requirements.txt

```text
flask
```

### 5.4 Dockerfile (Build Process)

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 80
CMD ["python", "app.py"]
```

#### Build Process Explanation

- Source code is pushed to GitHub
- Jenkins pulls the code from the repository
- Dockerfile creates the runtime environment
- Dependencies are installed inside the image
- The application is packaged into a Docker image

### 5.5 Jenkinsfile (Pipeline Definition in GitHub)

```groovy
pipeline {
    agent any

    environment {
        IMAGE_NAME = "your-dockerhub-username/myapp"
    }

    stages {

        stage('Clone Source') {
            steps {
                git 'https://github.com/your-username/my-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:latest .'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_TOKEN')]) {
                    sh 'echo $DOCKER_TOKEN | docker login -u your-dockerhub-username --password-stdin'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh 'docker push $IMAGE_NAME:latest'
            }
        }
    }
}
```

#### Jenkinsfile Explanation

- `pipeline` defines the CI/CD workflow
- `agent any` allows Jenkins to run the job on any available agent
- `environment` stores reusable pipeline variables
- `stages` groups the work into logical steps
- `git` clones the repository source code
- `docker build` creates the image
- `withCredentials` safely injects the Docker Hub token
- `docker push` uploads the image to Docker Hub

---

## 6. Part B: Jenkins Setup using Docker (Persistent Configuration)

### 6.1 Create Docker Compose File

The Jenkins container is started using Docker Compose so its configuration remains persistent across restarts.

```yaml
version: '3.8'

services:
  jenkins:
    image: jenkins/jenkins:lts
    container_name: jenkins
    restart: always
    ports:
      - "8082:8080"
      - "50001:50000"
    volumes:
      - jenkins_home:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock
    user: root

volumes:
  jenkins_home:
```

#### Docker Compose Explanation

- `jenkins/jenkins:lts` starts the stable Jenkins image
- `restart: always` ensures the container comes back after a reboot or crash
- `8082:8080` maps the Jenkins UI to port 8082 on the host
- `50001:50000` maps the Jenkins agent communication port
- `jenkins_home` persists Jenkins configuration and job data
- `/var/run/docker.sock` gives Jenkins access to the host Docker engine
- `user: root` avoids permission issues when Jenkins runs Docker commands

### 6.2 Start Jenkins

Run the compose file to start Jenkins:

```bash
docker compose up -d
```

![Docker Compose File](images/docker-compose-file.png)
![Compose Up](images/compose-up.png)

This command creates and starts the Jenkins container in detached mode.

Open Jenkins in the browser:

```text
http://localhost:8082
```

### 6.3 Unlock Jenkins

Retrieve the initial administrator password from inside the container:

```bash
docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

![Unlock Jenkins](images/unlock-jenkins.png)

This password is required for the first-time setup wizard.

### 6.4 Initial Setup

- Install the suggested plugins
- Create an admin user
- Complete the Jenkins setup wizard

![Jenkins Login](images/jenkins-login.png)

The login screen appears after Jenkins is started and unlocked successfully.

---

## 7. Part C: Jenkins Configuration

### 7.1 Add Docker Hub Credentials

Store the Docker Hub access token inside Jenkins instead of hardcoding it in the Jenkinsfile.

Path:

- Manage Jenkins -> Credentials -> Add Credentials

Recommended settings:

- Type: Secret Text
- ID: dockerhub-token
- Value: Docker Hub Access Token

#### Why this matters

Keeping secrets in Jenkins credentials protects them from source code exposure and makes the pipeline safer to share.

### 7.2 Create Pipeline Job

Create a new Jenkins pipeline job:

- New Item -> Pipeline
- Name: `ci-cd-pipeline`

Configure the job as:

- Pipeline script from SCM
- SCM: Git
- Repository URL: your GitHub repository
- Script Path: `Jenkinsfile`

#### Why this matters

Using Pipeline from SCM ensures the build logic lives in GitHub with the source code, so every change is version controlled.

---

## 8. Part D: GitHub Webhook Integration

### 8.1 Configure Webhook

In the GitHub repository settings:

- Go to Settings -> Webhooks -> Add Webhook
- Set the Payload URL to:

```text
http://<your-server-ip>:8082/github-webhook/
```

- Select `Push events`

#### Why this matters

The webhook allows GitHub to notify Jenkins automatically whenever code is pushed, which removes the need for manual build triggers.

---

## 9. Part E: Execution Flow (Stage-wise Explanation)

### Stage 1: Code Push

The developer updates the application or pipeline files in GitHub.

### Stage 2: Webhook Trigger

GitHub sends an event to Jenkins as soon as a push occurs.

### Stage 3: Jenkins Pipeline Execution

#### Stage: Clone

Jenkins pulls the latest source code from GitHub.

#### Stage: Build

Docker builds the image using the Dockerfile in the repository.

#### Stage: Auth

Jenkins logs in to Docker Hub using the stored token from credentials.

#### Stage: Push

The built image is pushed to Docker Hub.

### Stage 4: Artifact Ready

The Docker image is now available in Docker Hub and can be used for deployment anywhere.

---

## 10. Role of Same Host Agent

Jenkins runs inside Docker, and the Docker socket is mounted into the container:

```text
/var/run/docker.sock
```

### Effect

- Jenkins directly controls the host Docker daemon
- Builds and pushes can happen without a separate agent machine
- The setup is simple and suitable for lab use and small environments

---

## 11. Understanding Jenkins Pipeline Syntax (Simplified Explanation)

### 11.1 Common Steps

Most Jenkins pipelines follow this structure:

1. Define the pipeline
2. Choose an agent
3. Set environment variables
4. Add stages
5. Put shell or build commands inside each stage

### 11.2 The Challenging Part: `withCredentials`

`withCredentials` is used to safely access secrets during pipeline execution.

Example:

```groovy
withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_TOKEN')]) {
    sh 'echo $DOCKER_TOKEN | docker login -u your-dockerhub-username --password-stdin'
}
```

#### What it means

- Jenkins fetches the secret from its credential store
- It places the secret into a temporary environment variable
- The shell command uses the secret only inside the protected block
- The secret is not written directly in the Jenkinsfile

### 11.3 Simplified Version

Mentally, think of it like this:

```text
Get secret from Jenkins -> store it temporarily -> use it in the command -> discard it after the block
```

### 11.4 Why this is important

- Prevents hardcoding passwords or tokens
- Keeps the pipeline secure
- Makes the Jenkinsfile safe to publish in GitHub

---

## 12. Observations

- Jenkins GUI simplifies CI/CD management
- GitHub acts as both source repository and pipeline definition storage
- Docker ensures consistent and repeatable builds
- Webhooks enable automated pipeline execution
- Credentials stored in Jenkins improve security
- Docker socket mounting allows Jenkins to use the host Docker engine directly

---

## 13. Result

The CI/CD pipeline was successfully implemented with the following workflow:

- Source code and pipeline definition are maintained in GitHub
- Jenkins automatically detects changes using a webhook
- Docker image is built on the host Docker engine
- The image is securely pushed to Docker Hub

---

## 14. Key Takeaways

- Jenkins is GUI-based, but the pipeline is code-driven
- Always use Jenkins credentials instead of hardcoding secrets
- Webhook integration makes the process fully automatic
- Mounting the Docker socket allows Jenkins to use host Docker directly
- Keeping the Jenkinsfile in GitHub makes the workflow easy to version and review

---

## 15. Conclusion

This experiment demonstrates a practical CI/CD flow using Jenkins, GitHub, and Docker Hub. The setup shows how source control, automation, container builds, secret management, and webhook-triggered execution work together in a real pipeline.
