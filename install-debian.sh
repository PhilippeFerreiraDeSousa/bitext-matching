pip install virtualenv
sudo apt-get install yarn

cd back/
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

cd ../front/
yarn install
yarn start
