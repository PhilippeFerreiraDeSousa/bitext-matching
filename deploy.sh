sudo apt-get install apache2 apache2-dev python3 python3-dev
cd back/
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install -r requirements_prod.txt
python manage.py migrate

python manage.py collectstatic
python manage.py runmodwsgi
