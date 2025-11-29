# Dockerfile - builds an image that can run the preprocessing & upload scripts

#RUN apt-get update && apt-get install -y apt-utils
#RUN apt-get clean && apt-get update --allow-releaseinfo-change
#RUN apt-get update && apt-get install -y sudo

FROM python:3.11

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libgl1-mesa-glx \
        libglib2.0-0 \
        sudo \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src/ /app/src/
WORKDIR /app/src

COPY docker_entrypoint.sh /app/docker_entrypoint.sh
RUN chmod +x /app/docker_entrypoint.sh

ENTRYPOINT ["/app/docker_entrypoint.sh"]
