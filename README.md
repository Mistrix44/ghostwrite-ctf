# GHOSTWRITE: The Nightfall Incident — CTF Play Box

## Requirements
- Docker Engine
- Docker Compose

## Setup

1. Clone this repository.
2. Add these entries to `/etc/hosts` on Linux:

   127.0.0.1 nightfall-interactive.local
   127.0.0.1 forge.nightfall-interactive.local
   127.0.0.1 mirror-07.nightfall-interactive.local

3. Start the containers from the project root:

   docker compose up -d --build

4. Open CTFd at http://localhost:8000.
5. If CTFd displays the initial setup page, complete the setup.

## Restoring CTFd Data

The repository includes the exported CTFd data in:

`GHOSTWRITE_ The Nightfall Incident.zip`

1. Log in to CTFd as an administrator.
2. Navigate to the Admin Panel's Config section.
3. Find the import option.
4. Import the exported ZIP and follow the instructions.

**Warning:** Importing a backup can replace existing CTFd data. Use a fresh instance or back up any data you need to preserve.

After importing, verify that the six challenges, flags, hints, and configuration are present.

## Access

- CTFd admin panel: http://localhost:8000/admin
- Public entry point: http://localhost/
- SSH jump host: localhost, port 2222

## Challenges

1. **The Signal** — OSINT
   http://nightfall-interactive.local

2. **The Fake Fix** — Web Security
   http://localhost/verify/

3. **What Did They Run?** — Digital Forensics
   http://localhost/files/

4. **Under the Hood** — Programming/Scripting
   SSH tunnel and `exploit.py`

5. **The Compromised Host** — Linux/System Security
   SSH and systemd

6. **Follow the Ghost** — Networking
   `incident.pcap`

## Reset

To reset the entire environment and delete persistent Docker volumes:

    docker compose down -v
    docker compose up -d --build

**Warning:** This deletes persistent data, including the CTFd database.

To restart the Stage 4/5 service:

    docker compose restart stage45

## Acknowledgements

Built with Docker, Nginx, CTFd, Flask, Python, OpenSSH, and systemd.
