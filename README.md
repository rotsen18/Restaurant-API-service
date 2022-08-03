# Resaturant API service

Description

## Installation and launch

Python must already be installed on your system.
If you want to run locally, PostgreSQL server must be installed and a database must be created with the appropriate user

```shell
git clone https://github.com/rotsen18/Restaurant-API-service.git
cd Restaurant-API-service
python -m venv venv
venv/scripts/activate
pip install -r requirements.txt
set DB_HOST=<your db hostname>
set DB_NAME=<your db name>
set DB_USER=<your db username>
set DB_PASSWORD=<your db user password>
set SECRET_KEY=<your secret key>
python manage.py migrate
python manage.py runserver
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

* Adding restaurants
* Each restaurant has day menu
* Creating menu from dishes
* Voting for day menu for each restaurant (rate from 1 to 5)
* Getting day summary information (votes, rate)

## Usage

1.Create user and get token 
2.Create restaurant `POST /api/service/restaurant/`
3.Create dishes `POST /api/service/dishes/`
4.Create menu from dishes `POST /api/service/menus/`
5.Upload menu for restaurant `POST /api/service/restaurant/<restaurant_id>/current_menu/set/`
6.Get current menu for restaurant `GET /api/service/restaurant/<restaurant_id>/current_menu/`
7.Get summary information `GET /api/service/restaurant/<restaurant_id>/current_day_result/`
8.Vote for menu `POST /api/service/restaurant/<restaurant_id>/vote-current-menu/`
