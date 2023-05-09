# pull official base image
FROM python:3.8.3-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create directory for the app user
RUN mkdir -p /home/src/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV APP_HOME=/home/src/app
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add postgresql-dev 
RUN pip install --upgrade pip
COPY ./requirements.txt /home/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /home/src/app/

RUN chmod +x entrypoint.sh

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.prod.sh
ENTRYPOINT ["/home/src/app/entrypoint.sh"]