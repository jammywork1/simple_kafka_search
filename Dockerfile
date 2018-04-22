FROM python:3.6

WORKDIR /usr/src/app

# WORKDIR ~/

COPY *.py ./
RUN pip install --no-cache-dir confluent-kafka


ENTRYPOINT [ "python", "./main.py" ]   