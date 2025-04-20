Server Set up in EC2

import os

ALLOWED_HOSTS = ['13.49.225.87', 'localhost']
DEBUG = False
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [] if you have staticfiles
Connect with your pem file to servers from terminal 
chmod 400 your-key.pem
ssh -i django.pem ubuntu@13.49.225.87

sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx git -y

cd ~
git clone https://github.com/nagusuresh/djangoo...  
python3 -m venv venv  
source venv/bin/activate  
pip install --upgrade pip
pip install django 
cd your-django-project
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
add security group 0.0.0.0:8000
python manage.py runserver 0.0.0.0:8000
Now test with 13.49.225.87:8000


nginx - it is a webserver it supports webpage

gunicorn
will create socket which helps to runserver without command

pip install gunicorn


sudo nano /etc/nginx/sites-available/school

server {
    listen 80;
    server_name 54.152.144.173;

    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /home/ubuntu/school/staticfiles/;
        autoindex on;
    }
}

# ln refers to softlink where this setting link to sites-enabled as default
sudo ln -s /etc/nginx/sites-available/school /etc/nginx/sites-enabled
sudo nginx -t  
sudo systemctl restart nginx  
sudo ufw allow 'Nginx Full'  #it will allow the firewall trafiic

sudo nano /etc/systemd/system/gunicorn.service

[Unit]
Description=Gunicorn Daemon for Django
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/school
ExecStart=/usr/bin/pipenv run gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock school.wsgi:application

Ensure the socket file is created
RuntimeDirectory=gunicorn
RuntimeDirectoryMode=755

[Install]
WantedBy=multi-user.target

sudo systemctl start gunicorn  
sudo systemctl enable gunicorn 

sudo systemctl status gunicorn  
sudo systemctl status nginx  

for errors check

Issue One: (Socket not created)
sudo chown ubuntu:www-data /run/
sudo chmod 775 /run/
sudo systemctl restart gunicorn

Issue Two: (admin static file permissions )
sudo chown -R ubuntu:www-data /home/ubuntu/school/staticfiles
sudo chmod -R 755 /home/ubuntu/school/staticfiles
sudo chmod +x /home/ubuntu
sudo chmod +x /home/ubuntu/school

Error log:
sudo tail -f /var/log/nginx/error.log


Integrate PostgreSQL with Django on AWS EC2 


sudo apt install postgresql postgresql-contrib -y

sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl status postgresql  

sudo -i -u postgres
psql

CREATE DATABASE testproject;
CREATE USER django WITH PASSWORD 'mypassword';
ALTER ROLE django SET client_encoding TO 'utf8';
ALTER ROLE django SET default_transaction_isolation TO 'read committed';
ALTER ROLE django SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE testproject TO django;

\q
exit

sudo nano /etc/postgresql/14/main/postgresql.conf
listen_addresses = '*'

sudo nano /etc/postgresql/14/main/pg_hba.conf
host    all             all             0.0.0.0/0               md5

sudo systemctl restart postgresql

Go to AWS Console → EC2 → Security Groups.
Select the Security Group for your EC2 instance.
Click Edit inbound rules.
Add Rule:

    Type: PostgreSQL
    Protocol: TCP
    Port Range: 5432
    Source: 0.0.0.0/0 

update in setting.py page

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'testproject',
        'USER': 'django',
        'PASSWORD': 'mypassword',
        'HOST': '13.49.225.87',
        'PORT': '5432',
    }
}

source /home/ubuntu/djangoone/venv/bin/activate
pip install psycopg

sudo systemctl restart gunicorn
sudo systemctl restart nginx
python manage.py migrate





