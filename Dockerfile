FROM python:3.8.10

ENV APP_PORT=8000

COPY requirements.txt /tmp

RUN pip3 install -r /tmp/requirements.txt

RUN mkdir -p /api

COPY . /api

WORKDIR /api

CMD ["./scripts/uvicorn"]
