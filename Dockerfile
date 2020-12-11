# Dockerfile for csm-ssh-keys
# Copyright 2019-2020 Hewlett Packard Enterprise Development LP

FROM dtr.dev.cray.com/baseos/alpine:3.12.0 as service
WORKDIR /app
RUN mkdir /app/src
COPY /src/ /app/src
COPY /src/csmsshkeys /app/src/csmsshkeys
COPY setup.py README.md .version /app/
ADD constraints.txt requirements.txt /app/
RUN apk add --no-cache linux-headers gcc g++ python3-dev py3-pip musl-dev libffi-dev openssl-dev git jq curl openssh-client
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir . && \
    rm -rf /app/*
ENTRYPOINT [ "python3", "-m", "csmsshkeys" ]
