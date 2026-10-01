FROM debian:12-slim
RUN apt-get update && apt-get install -y openssh-server && rm -rf /var/lib/apt/lists/*
RUN useradd -m -s /bin/bash player
RUN mkdir -p /home/player/.ssh
COPY player_key.pub /home/player/.ssh/authorized_keys
RUN chown -R player:player /home/player/.ssh && chmod 700 /home/player/.ssh && chmod 600 /home/player/.ssh/authorized_keys
RUN mkdir -p /run/sshd
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
