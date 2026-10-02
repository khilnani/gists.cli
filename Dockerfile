FROM python:2-alpine

# A Docker image for gists.cli
# https://github.com/khilnani/gists.cli

RUN pip install gists.cli
RUN adduser -Dh /gists gists


USER gists
WORKDIR /gists

ENTRYPOINT [ "/usr/local/bin/gists" ]
