FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update && \
    apt-get install -y systemd systemd-sysv openssh-server sudo python3 python3-pip python3-flask curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN systemctl mask \
    systemd-udevd.service dev-hugepages.mount sys-fs-fuse-connections.mount \
    systemd-remount-fs.service getty.target

RUN mkdir -p /run/sshd
RUN rm -f /etc/update-motd.d/* /etc/legal
COPY motd /etc/motd

# --- ghost-diag service (Stage 4) ---
RUN mkdir -p /opt/ghost-diag
COPY ghost-diag.py /opt/ghost-diag/app.py
COPY ghost-diag.service /etc/systemd/system/ghost-diag.service
RUN systemctl enable ghost-diag.service

# --- Standard non-root player account (Stage 5 access) ---
RUN useradd -m -s /bin/bash player && \
    mkdir -p /home/player/.ssh
COPY player_key_stage5.pub /home/player/.ssh/authorized_keys
RUN chown -R player:player /home/player/.ssh && \
    chmod 700 /home/player/.ssh && \
    chmod 600 /home/player/.ssh/authorized_keys

# --- Decoy accounts: legitimate-looking, but not the real persistence ---
RUN useradd -r -m -s /usr/sbin/nologin svc-backup && \
    useradd -r -m -s /usr/sbin/nologin build-agent && \
    usermod -aG docker build-agent 2>/dev/null || true

# --- The attacker's persistence account ---
RUN useradd -r -m -s /bin/bash ghostwrite && \
    usermod -aG sudo ghostwrite

# --- The persistence mechanism players must find ---
RUN mkdir -p /opt/.sync
COPY sync.sh /opt/.sync/sync.sh
RUN chmod 755 /opt/.sync/sync.sh && chown ghostwrite:ghostwrite /opt/.sync/sync.sh
COPY ghost-sync.service /etc/systemd/system/ghost-sync.service
RUN systemctl enable ghost-sync.service
COPY backup-sync.service /etc/systemd/system/backup-sync.service
RUN systemctl enable backup-sync.service
STOPSIGNAL SIGRTMIN+3
ENTRYPOINT ["/sbin/init"]
