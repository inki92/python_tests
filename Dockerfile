FROM python:3.6

COPY \
  requirements.txt /etc/

RUN \
  pip install --upgrade pip && \
  pip install -r /etc/requirements.txt

RUN \
  apt-get update && \
  apt-get install -y redis-server && \
  rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH "${PYTHONPATH}:/opt/app"

ENTRYPOINT service redis-server start && python -m rest
