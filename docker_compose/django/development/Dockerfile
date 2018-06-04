FROM python:2

ENV PYTHONUNBUFFERED 1

# Setup Debian linux
RUN export DEBIAN_FRONTEND=noninteractive

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY requirements.txt ./
RUN pip install -r requirements.txt

WORKDIR /usr/src/app

RUN groupadd -r django \
  && useradd -r -g django django \
  && mkdir static \
  && chown -R django static \
  && chmod -R 755 static

COPY . .


COPY ./docker_compose/django/development/start.sh /start.sh
COPY ./docker_compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
  && sed -i 's/\r//' /start.sh \
  && chmod +x /entrypoint.sh \
  && chmod +x /start.sh

ENTRYPOINT ["/entrypoint.sh"]
