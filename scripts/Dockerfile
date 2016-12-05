FROM ubuntu:trusty

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_TERSE true

RUN mkdir -p /app
WORKDIR /app


RUN apt-get -q update && apt-get -q install --no-install-recommends -y \
  python \
  python2.7 \
  python-pip


COPY *.py *.txt /app/

RUN chmod 755 *.py
RUN pip install   -r requirements.txt
