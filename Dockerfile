FROM alpine

COPY entrypoint.sh /entrypoint.sh

RUN apk add --update bash \
  curl \
  git \
  grep \
  jq

ENTRYPOINT ["/entrypoint.sh"]
