#!/bin/sh


echo "The postgres host  is: $POSTGRES_HOST $POSTGRES_DB_PORT"
# Wait for the DB to be ready
until nc -z -v -w30 $POSTGRES_HOST $(( $POSTGRES_DB_PORT ));
do
 echo 'Waiting for the DB to be ready...'
 sleep 2
done

python manage.py makemigrations
python manage.py migrate
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
from accounts.models import Profile
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin@example.com', 'admin', 'John', 'Doe', 'admin')
    Profile.objects.create(user=user, gender='male', date_of_birth='2003-05-31', bio='biography', info='info')
EOF
python manage.py runserver 0.0.0.0:8000
