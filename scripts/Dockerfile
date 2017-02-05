FROM ubuntu:trusty

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_TERSE true

RUN mkdir -p /app
WORKDIR /app


RUN apt-get -q update && apt-get -q install --no-install-recommends -y \
  python2.7 \
  python-pip \
  python-dev \
  gcc

RUN pip install -U pip

COPY requirements.txt /app/
RUN pip install -r requirements.txt

VOLUME [ "/app" ]

CMD ["/app/start"]
