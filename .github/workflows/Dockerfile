FROM ubuntu:22.04
ENV container docker

# Install systemd and dependencies
RUN apt-get update && apt-get install -y systemd systemd-sysv python3 python3-pip

# Install Poetry
RUN pip3 install poetry

# Disable certain systemd services that don't make sense in a container
RUN systemctl mask \
    dev-hugepages.mount \
    sys-fs-fuse-connections.mount \
    sys-kernel-config.mount \
    display-manager.service \
    getty@.service \
    systemd-logind.service \
    systemd-remount-fs.service \
    getty.target \
    graphical.target

# Enable lingering for the root user so that user-level systemd units can run
RUN loginctl enable-linger root

# Copy your code into the container
WORKDIR /app
COPY .. /app

# Install Python dependencies using Poetry
RUN poetry install

VOLUME [ "/sys/fs/cgroup" ]

CMD [ "/lib/systemd/systemd" ]
