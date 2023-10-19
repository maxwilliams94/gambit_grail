FROM python:3.11.6-alpine

RUN apk update && apk add git

WORKDIR /
ARG BRANCH="main"
RUN git clone --branch ${BRANCH} https://github.com/maxwilliams94/gambit_grail.git gambit_grail

ENV GAMBIT_PGN=/gambit_grail/src/gambit/gambits.pgn

WORKDIR /gambit_grail
RUN python -m pip install .

WORKDIR /gambit_grail/src/gambit
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]