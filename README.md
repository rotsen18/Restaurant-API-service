# Resaturant API service

Description

## Installation and launch

Python must already be installed on your system

```shell

```

If you want to activate debug option you may set env
```shell
set DEBUG=True
```

## Run with docker

Docker should be installed

```shell
docker-compose build
docker-compose up
```

## Getting access

All documentation in two different styles is located at:
* /api/doc/swagger/
* /api/doc/redoc/

- create user at `/api/user/register/`
- get access token on `/api/user/token/`
- now every request should contain header:
`Authorisation: Bearer <your access token>`

for update access token you should post your refresh token at:
`/api/user/token/refresh/`

If you want to create admin user you should add superuser with command:
```shell
python manage.py createsuperuser
```

## Features

* 
