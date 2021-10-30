FROM python:3.9-slim 

ENV INSTALL_PATH /pos
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

RUN apt-get update && apt-get install -qq -y build-essential libpq-dev --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 

COPY . . 

CMD gunicorn -w 4 -b 0.0.0.0:${PORT} --access-logfile - "api.all:create_app()"