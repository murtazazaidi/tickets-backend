# Tickets
Peer to peer task assignment system based on Django Rest Framework.

## Description
This is a simplistic private task assignment system where multiple users can create and assign tasks to each other. The tasks (tickets) will only be editable by the reporter and will only be visible to reporter and assignee.

## Setup
```
git clone https://github.com/murtazazaidi/tickets-backend.git
cd tickets-backend
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
echo "SECRET_KEY = 'some secret key'" > project/config.py
python manage.py makemigrations tickets
python manage.py migrate
```
