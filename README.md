# URL-Shortener

[![CircleCI](https://circleci.com/gh/karolina-kozicka/URL-Shortener/tree/master.svg?style=shield&circle-token=6ade352773cfb70bb89fefc6933a328fdc7aec4b)](https://circleci.com/gh/karolina-kozicka/URL-Shortener/tree/master)
<!-- 
### Table of contents
* [General info](#general-info)
* [Setup](#setup) -->

## General information

URL-Shortener - Web application to shorten links with possibility to define expiration date and password to protect your content.

Most of code is written in Python/Django.


***
## Setup

Project can be run in local (`local.yml`) or production (`production.yml`) mode.

### Requirements
To setup project it is required to have [Docker](https://docs.docker.com) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine.

### Build

    $ docker-compose -f <mode>.yml build

### Database migrations

    $ docker-compose -f <mode>.yml run django python app/manage.py migrate

### Creating superuser
Optionally you might also want to create django superuser.

    $ docker-compose -f <mode>.yml run django python app/manage.py createsuperuser

### Run tests
    $ docker-compose -f <mode>.yml run django python app/manage.py test shortener

### Fixtures data

    $ docker-compose -f <mode>.yml run django python app/manage.py loaddata celery_beat

`celery_beat` file contains periodic tasks definitions.

### Start server

    $ docker-compose -f <mode>.yml up

It will start all containers on specified environment.

URL-Shortener is now available on [localhost:8000](http://localhost:8000)

***