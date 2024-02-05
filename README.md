# Registration App

Basic registration app. Built with Django + VueJS3

Following must be installed:

- Docker

Steps to run:

1. Create `.env` file and copy contents of `env.example`
2. Change value of `SECRET_KEY` to some random string if needed.
3. Run project with command `docker compose up --build -d`
4. Open `http://localhost:8000` on a web browser to access the app
5. To view API documentation via swagger, visit `http://localhost:8000/api/swagger/`

To run via docker:

```
docker compose up --build -d
```

To migrate database:

```
docker compose run --rm backend ./manage.py migrate
```

To create superuser:

```
docker compose run --rm backend ./manage.py createsuperuser
```

To run tests:

```
docker compose run --rm backend pytest
```

To run tests with coverage:

```
docker compose run --rm backend --cov=apps apps/registration/tests/ --cov-report html
```

To stop containers:

```
docker compose down
```
