FROM alpine:3.11

COPY entrypoint.py /entrypoint.py

RUN apk add --update \
  git \
  py3-pip

RUN pip3 install gitpython PyGithub

ENTRYPOINT ["/entrypoint.py"]
