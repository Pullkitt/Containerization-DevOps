
**Name:** Pulkit Jain  
**SAP ID:** 500121477  
**Batch:** B3 (CCVT)

# Lab – Experiment 1

## Objective
- To understand the conceptual and practical differences between Virtual Machines and Containers.
- To install and configure a Virtual Machine using VirtualBox and Vagrant on Windows.
- To install and configure Containers using Docker inside WSL.
- To deploy an Ubuntu-based Nginx web server in both environments.
- To compare resource utilization, performance, and operational characteristics of VMs and Containers.

---
## Software and Hardware Requirements
### Hardware
- 64-bit system with virtualization support enabled in BIOS
- Minimum 8 GB RAM (4 GB minimum acceptable)
- Internet connection

### Software (Windows Host)
- Oracle VirtualBox
- Vagrant
- Windows Subsystem for Linux (WSL 2)
- Ubuntu (WSL distribution)
- Docker Engine (docker.io)

### Software (macOS – for troubleshooting/reference)
- Oracle VirtualBox (Intel Macs only)
- Vagrant
- Docker Desktop (alternative if WSL is not applicable)

---
## Theory
### Virtual Machine (VM)
A Virtual Machine emulates a complete physical computer, including its own operating system kernel, hardware drivers, and user space. Each VM runs on top of a hypervisor.

**Characteristics:**
- Full OS per VM
- Higher resource usage
- Strong isolation
- Slower startup time

### Container
Containers virtualize at the operating system level. They share the host OS kernel while isolating applications and dependencies in user space.

**Characteristics:**
- Shared kernel
- Lightweight
- Fast startup
- Efficient resource usage

---
## Experiment Setup – Part A: Virtual Machine (Windows)

**Step 1: Install VirtualBox**
Download VirtualBox from the official website. Run the installer and keep default options. Restart the system if prompted.

**Step 2: Install Vagrant**
Download Vagrant for Windows. Install using default settings. Verify installation:

```bash
vagrant --version
```
![Vagrant Version](images/vagversion.png)

**Step 3: Create Ubuntu VM using Vagrant**
Create a new directory and initialize Vagrant:
```bash
mkdir vm-lab
cd vm-lab
vagrant init ubuntu/jammy64
```
![Vagrant Init](images/vaginit-up.png)

Start the VM:
```bash
vagrant up
```
![Vagrant Up](images/vaginit-up.png)

Access the VM:
```bash
vagrant ssh
```
![Vagrant SSH](images/vagssh.png)

**Step 4: Install Nginx inside VM**
```bash
sudo apt update
sudo apt install -y nginx
sudo systemctl start nginx
```
![Start Nginx in VM](images/vagstartnginx.png)

**Step 5: Verify Nginx**
```bash
curl localhost
```
![Curl Localhost](images/curllocal.png)

**Stop and remove VM**
```bash
vagrant halt
```
![Vagrant Halt](images/vaghalt.png)
```bash
vagrant destroy
```
![Vagrant Destroy](images/vagdestory.png)

---
## Experiment Setup – Part B: Containers using WSL (Windows)


**Step 1: Install WSL 2**
```bash
wsl --install
```
![Install WSL](images/wsl-ubuntu.png)

**Step 2: Install Ubuntu on WSL**
```bash
wsl --install -d Ubuntu
```
![Install Ubuntu on WSL](images/wsl-ubuntu.png)

**Step 3: Install Docker Engine inside WSL**
```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo usermod -aG docker $USER
# Logout and login again to apply group changes
```
![Step 3 WSL](images/step3wsl.png)

**Step 4: Run Ubuntu Container with Nginx**
```bash
docker pull ubuntu
```
![Docker Pull](images/dockerpull.png)
```bash
docker run -d -p 8080:80 --name nginx-container nginx
```
![Run Nginx Container](images/dockrunnginx.png)

**Step 5: Verify Nginx in Container**
```bash
curl localhost:8080
```
![Curl Localhost 8080](images/curllocal.png)

---
## Resource Utilization Observation


### VM Observation Commands
```bash
free -h
htop
systemd-analyze
```
![VM Observation](images/vmobservation.png)

### Container Observation Commands
```bash
docker stats
```
![Docker Stats](images/dockstats.png)
```bash
free -h
```
![Docker Free](images/dockfree.png)

| Parameter      | Virtual Machine | Container |
|---------------|----------------|-----------|
| Boot Time     | High           | Very Low  |
| RAM Usage     | High           | Low       |
| CPU Overhead  | Higher         | Minimal   |
| Disk Usage    | Larger         | Smaller   |
| Isolation     | Strong         | Moderate  |

---
## Result
The experiment demonstrates that containers are significantly more lightweight and resource-efficient compared to virtual machines, while virtual machines provide stronger isolation and full OS-level abstraction.
---
## Conclusion
Virtual Machines are suitable for full OS isolation and legacy workloads, whereas Containers are ideal for microservices, rapid deployment, and efficient resource utilization.
---

---
## References
- VirtualBox Documentation
- Vagrant Documentation
- Docker Official Documentation
