# Tickets
Peer to peer task assignment system based on Django Rest Framework.

## Description
This is a simplistic private task assignment system where multiple users can create and assign tasks to each other. The tasks (tickets) will only be editable by the reporter and will only be visible to reporter and assignee.

## Basic Setup
```
git clone https://github.com/murtazazaidi/tickets-backend.git
cd tickets-backend

echo "SECRET_KEY=some_secret_key" > .env
echo "DEBUG=True" >> .env
echo "ALLOWED_HOSTS=localhost, 127.0.0.1, 0.0.0.0" >> .env

echo "POSTGRES_PASSWORD=[postgres_password]" >> .env
echo "POSTGRES_USER=[postgres_user]" >> .env
echo "POSTGRES_DB=tickets" >> .env

echo "DATABASE_URL=postgres://[postgres_user]:[postgres_password]@localhost:5432/tickets" >> .env
```

## To Run Locally
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py makemigrations tickets
python manage.py migrate
```

## To Run in Docker Container
```
docker-compose build
docker-compose up -d
```
