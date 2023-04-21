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
docker-compose up --build
```
*if "exec ./entrypoint.sh: no such file or directory", do this:
```
git config --global core.autocrlf input
git rm --cached -r .
git reset --hard
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
docker exec inforce_tt-dev-1 python manage.py test
```

Command, to create superuser:
```
docker exec -it inforce_tt-dev-1 python manage.py createsuperuser
```