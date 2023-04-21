## Test task for Inforce company

Used:

```
- Django
- DRF
- JWT
- PostgreSQL
- Docker(docker-compose)
```

Usage:

```
git clone https://github.com/ExSumbiT/Inforce_TT.git
cd Inforce_TT
# create venv >python -m venv venv
# >venv/Scripts/activate or >source venv/bin/activate
pip install -r requirements.txt
```

Apply migrations:

```
docker-compose run --rm dev python manage.py makemigrations
docker-compose run --rm dev python manage.py migrate
```

Run project in docker:

```
docker-compose up dev
```

Endpoints:
```
api/v1/auth/token/ - Authentication
api/v1/auth/token/refresh/ - Refresh JWT Token
api/v1/employee/create/ - Creating employee (Need to be a superuser)
api/v1/restaurant/create/ - Creating restaurant (Need to be a superuser)
api/v1/restaurant/menu/upload/ - Uploading menu for restaurant (Need to be a restaurant)
api/v1/restaurant/menu/today/ - Getting current day menu (Need to be a user)
api/v1/restaurant/vote/ - Vote for menu (Need to be a user)
api/v1/restaurant/vote/today/ - Getting results for the current day (Need to be a user)
```

Command, to run tests:
```
docker-compose run --rm dev python manage.py test
# or
cd lunch_decision
python manage.py test
```

Command, to create superuser:
```
docker-compose run --rm dev python manage.py createsuperuser
# or
cd lunch_decision
python manage.py createsuperuser
```