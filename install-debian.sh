#!/bin/bash

echo -e "\e[1m\e[34mBienvenue sur le script d'installation de l'aligneur de bitextes"
echo -e "Ce script est destiné aux distributions Ubuntu-like. \e[31mUn compte GitHub est nécessaire.\e[0m"
read -p "Adresse mail du compte GitHub : " mail
read -p "Prénom Nom : " name

### INSTALL ###
echo -e "\e[1m\e[34mInstallation des dépendances...\e[0m"
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo -E apt-get update
sudo -E apt-get install -y python3-pip apt-transport-https yarn # atom qtcreator

cd back/
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
python manage.py migrate
python manage.py loaddata bitexts
python manage.py runserver

cd ../front/
yarn install
yarn start
