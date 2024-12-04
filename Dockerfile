FROM alpine:3.20

COPY entrypoint.py /entrypoint.py

RUN apk add --update --no-cache \
  git \
  py3-pip

RUN pip3 install --break-system-packages \
  gitpython \
  PyGithub==v1.54.1 \
  pylint

ENTRYPOINT ["/entrypoint.py"]
