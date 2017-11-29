#!/bin/bash

echo -e "\e[1m\e[34mBienvenue sur le script d'installation de l'aligneur de bitextes"
echo -e "Ce script est destiné aux distributions Ubuntu-like. \e[31mUn compte GitHub est nécessaire.\e[0m"
read -p "Adresse mail du compte GitHub : " mail
read -p "Prénom Nom : " name

### INSTALL ###
echo -e "\e[1m\e[34mInstallation des dépendances...\e[0m"
sudo -E apt-get update
sudo -E apt-get install -y python-pip yarn # atom qtcreator

cd back/
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

cd ../front/
yarn install
yarn start
