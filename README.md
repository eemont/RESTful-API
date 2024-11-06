# RESTful-API

 Building a RESTful API with Flask : Error Handling, Authentication, and File Handling with Public and Admin Routes

## Members :

<li>Emmanuel Montoya</li>
<li>Renzo Salosagcol</li>
<li>Anthony Weathersby</li>

## Introduction :
In this mid-project, we built a RESTful API using Flask, implementing comprehensive error handling, user authentication, and file handling capabilities. The API includes two route types: public routes, accessible without authentication, and protected admin routes that require secure authentication. Through this project, we developed a robust API structure that effectively manages errors, ensures secure user access, and supports file uploads.

## Installation and Setup

### Requirements:
- VS Code
- Python 3.8 or higher
- MySQL
- WSL

## 1. Create and set up Virtual Environment
### create project directory
mkdir flask_api_project
cd flask_api_project

### Create Virtual Environment
sudo apt update
sudo apt install python3-venv
python3 -m venv venv

### Activate Virtual Environment
source venv/bin/activate

## 2. Install MySQL and Configure
### Install required packages
sudo apt-get update
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config

### Install MySQL
sudo apt-get install mysql-server

### Create MySQL directories with proper permissions
sudo mkdir -p /var/run/mysqld
sudo chown mysql:mysql /var/run/mysqld
sudo chmod 777 /var/run/mysqld

sudo mkdir -p /var/lib/mysql
sudo chown mysql:mysql /var/lib/mysql

### Start MySQL service
sudo service mysql start

## 3. Set Up MySQL Database and User
### Access MySQL as root
sudo mysql

### In MySQL prompt, run:
CREATE DATABASE flask_api_db;
CREATE USER 'flaskuser'@'localhost' IDENTIFIED BY 'flaskpassword';
GRANT ALL PRIVILEGES ON flask_api_db.* TO 'flaskuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;

### Verify connection
mysql -u flaskuser -p
Enter password: flaskpassword

## 4. Install Python Dependencies
pip install -r requirements.txt

## 5. Run Flask Application
python3 main.py

## Possible Permission Issues Solution
sudo chown -R mysql:mysql /var/run/mysqld
sudo chmod -R 755 /var/run/mysqld
