
FROM mongo:4.2-bionic
LABEL maintainer="stevenmi - Steven Mi <s0558366@htw-berlin.de>"

# Python
ARG PYTHON_VERSION=3.7

# Set enviroment variables
ENV LANG=C.UTF-8

# Install python and pip
RUN apt-get update \
    && apt-get install -y \
            git \
            nano \
            python${PYTHON_VERSION} \
            python3-pip \
            cron \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pymongo \
    && pip3 install pandas \
    && pip3 install python-crontab

# Copy scripts into container
COPY ./scripts /scripts
RUN python3 /scripts/CSV-to-MongoDB-scheduler.py

# Define variables to be used
VOLUME ["/data/db"]
EXPOSE 27017

# Define working directory.
WORKDIR /data
