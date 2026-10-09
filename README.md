# GHOSTWRITE: The Nightfall Incident — CTF Play Box

## Setup
1. Install Docker and Docker Compose on a Linux host (built and
   tested on Ubuntu, VirtualBox VM).
2. Clone this repository.
3. Add these lines to your hosts file (needed for Stage 1's fake
   domains to resolve):
   127.0.0.1   nightfall-interactive.local
   127.0.0.1   forge.nightfall-interactive.local
   127.0.0.1   mirror-07.nightfall-interactive.local
4. From the project root, run:
   docker compose up -d
5. CTFd admin panel: http://localhost:8000/admin
   Public entry point (proxy): http://localhost/
   SSH jump host: localhost, port 2222

## Reset
To reset the whole box to a clean state:
   docker compose down -v
   docker compose up -d --build
This rebuilds every container fresh and recreates the databases.

To reset a single stage (example: Stage 4/5 host):
   docker compose restart stage45

## Stages
1. The Signal — OSINT — http://nightfall-interactive.local
2. The Fake Fix — Web Security — http://localhost/verify/
3. What Did They Run? — Digital Forensics — http://localhost/files/
4. Under the Hood — Programming/Scripting — SSH tunnel + exploit.py
5. The Compromised Host — Linux/System Security — SSH, systemd
6. Follow the Ghost — Networking — incident.pcap

## Acknowledgements
Built with Docker, Nginx, CTFd, Flask, Python, OpenSSH, systemd.
