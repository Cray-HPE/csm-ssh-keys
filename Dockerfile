#
# MIT License
#
# (C) Copyright 2019-2022, 2025 Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# Dockerfile for csm-ssh-keys

FROM artifactory.algol60.net/csm-docker/stable/docker.io/library/alpine:3.21 AS service
WORKDIR /app
ENV VIRTUAL_ENV=/app/venv
RUN apk add --upgrade --no-cache apk-tools &&  \
	apk update && \
	apk add --no-cache linux-headers gcc g++ python3 python3-dev py3-pip musl-dev libffi-dev openssl-dev git jq curl openssh-client && \
	apk -U upgrade --no-cache && \
    mkdir /app/src && \
    python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ADD constraints.txt requirements.txt /app/
COPY /src/ /app/src
COPY /src/csmsshkeys /app/src/csmsshkeys
COPY setup.py README.md .version gitInfo.txt /app/
RUN --mount=type=secret,id=netrc,target=/root/.netrc \
    pip3 list --format freeze && \
    pip3 install --no-cache-dir --upgrade pip -c constraints.txt && \
    pip3 install --no-cache-dir --disable-pip-version-check --upgrade setuptools wheel -c constraints.txt && \
    pip3 list --format freeze && \
    pip3 install --no-cache-dir --disable-pip-version-check --ignore-installed six -r requirements.txt && \
    pip3 install --no-cache-dir --disable-pip-version-check . -c constraints.txt && \
    pip3 list --format freeze && \
    rm -rvf /app/src /app/setup.py /app/*.txt /app/.version /app/README.md
USER nobody:nobody
ENTRYPOINT [ "python3", "-m", "csmsshkeys" ]
