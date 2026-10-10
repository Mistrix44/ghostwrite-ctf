# GHOSTWRITE: The Nightfall Incident — CTF Play Box

GHOSTWRITE is a multi-stage Capture the Flag (CTF) environment built using CTFd and Docker. It contains six challenges covering OSINT, web security, digital forensics, scripting, Linux security, and network analysis.

## Requirements

- Linux host (Ubuntu recommended)
- Docker Engine
- Docker Compose
- Git

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Mistrix44/ghostwrite-ctf.git
cd ghostwrite-ctf
```

### 2. Configure Hostnames

Add the following entries to `/etc/hosts` on your Linux machine:

```text
127.0.0.1 nightfall-interactive.local
127.0.0.1 forge.nightfall-interactive.local
127.0.0.1 mirror-07.nightfall-interactive.local
```

These hostnames are required for the Stage 1 OSINT challenge.

### 3. Start the Environment

From the project root, run:

```bash
docker compose up -d --build
```

Check that the containers are running:

```bash
docker compose ps
```

### 4. Access CTFd

Open the following addresses in your browser:

- CTFd: http://localhost:8000
- Public challenge entry point: http://localhost/

If CTFd displays the initial setup page, complete the setup to create an administrator account before importing the event.

## Restoring the GHOSTWRITE Event

The repository includes the exported CTFd event:

`GHOSTWRITE_ The Nightfall Incident.zip`

### Import Instructions

1. Start the Docker environment.
2. Open http://localhost:8000.
3. Log in to CTFd as an administrator.
4. Open the Admin Panel and navigate to the configuration or backup section.
5. Locate the import option.
6. Select the exported ZIP file and follow the import instructions.
7. After importing, verify that all six challenges and their associated data are present.

**Important:** Importing a backup can replace existing CTFd data. Use a fresh instance and back up any important data before importing.

The export restores CTFd data, but custom challenge services must also be running. Verify that the required Docker containers are running after the import.

## Challenge Stages

### Stage 1 — The Signal
**Category:** OSINT

Investigate the clues and information associated with the Nightfall Interactive environment.

Entry point: http://nightfall-interactive.local

### Stage 2 — The Fake Fix
**Category:** Web Security

Investigate the web challenge and identify the intended vulnerability.

Entry point: http://localhost/verify/

### Stage 3 — What Did They Run?
**Category:** Digital Forensics

Examine the available evidence and investigate the activity associated with the incident.

Entry point: http://localhost/files/

### Stage 4 — Under the Hood
**Category:** Programming and Scripting

Investigate the target through the provided SSH tunnel and work with `exploit.py`.

### Stage 5 — The Compromised Host
**Category:** Linux and System Security

Investigate the compromised Linux environment, including relevant SSH and systemd components.

### Stage 6 — Follow the Ghost
**Category:** Network Forensics

Analyze the provided network capture:

`incident.pcap`

## Service Access

| Service | Address |
|---|---|
| CTFd | http://localhost:8000 |
| Public entry point | http://localhost/ |
| Stage 1 | http://nightfall-interactive.local |
| Stage 2 | http://localhost/verify/ |
| Stage 3 | http://localhost/files/ |
| SSH jump host | localhost:2222 |

Some stages require access to additional services or files provided by the environment.

## Resetting the Environment

To stop the environment and remove its persistent Docker volumes:

```bash
docker compose down -v
```

To rebuild and start the environment again:

```bash
docker compose up -d --build
```

**Warning:** The `docker compose down -v` command deletes persistent volumes, including the CTFd database and other stored data. Export or back up any important information before running it.

To restart the Stage 4/5 service without resetting the entire environment:

```bash
docker compose restart stage45
```

## Troubleshooting

### Containers Are Not Running

Check their status:

```bash
docker compose ps
```

View the CTFd logs:

```bash
docker compose logs --tail=100 ctfd
```

### CTFd Displays the Initial Setup Page

This can happen when CTFd starts with a new database. Complete the initial setup, then import the supplied event export.

### A Challenge Website Is Unavailable

Check the container status and logs:

```bash
docker compose ps
docker compose logs --tail=100
```

Also verify that the required hostnames are present in `/etc/hosts`.

## Technologies Used

- CTFd
- Docker and Docker Compose
- Nginx
- Flask
- Python
- OpenSSH
- Linux and systemd
- Network traffic analysis tools

## Acknowledgements

Developed as a multi-stage cybersecurity CTF project for hands-on security learning and investigation.
