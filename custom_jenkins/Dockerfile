# Jenkins LTS (Debian bookworm)
FROM jenkins/jenkins:lts

# Switch to root
USER root

# Install Docker (recommended way for containers)
RUN apt-get update && \
    apt-get install -y \
        ca-certificates \
        curl \
        docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add Jenkins user to docker group
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Docker data directory
VOLUME /var/lib/docker

# Back to Jenkins user
USER jenkins
