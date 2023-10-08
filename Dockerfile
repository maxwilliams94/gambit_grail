FROM python:3.11.6-alpine

RUN apk update && apk add git

WORKDIR /src
ARG BRANCH="main"
RUN git clone --branch ${BRANCH} https://github.com/maxwilliams94/gambit_grail.git gambit_grail

WORKDIR /src/gambit_grail
RUN python -m pip install .
COPY run.sh /

CMD ["sh", "/run.sh"]