# Fields service [![Build Status](https://travis-ci.org/lv-412-python/4m-fields-service.svg?branch=develop)](https://travis-ci.org/lv-412-python/4m-fields-service) 
## Description
This is the source code of the fields service, part of 4m project. This service stores fields from which forms will be created. 

## Technologies
* Python (3.6.8)
* Flask (1.0.3)
* PostgreSQL (10.8)

## Install
For the next steps of service installation, you will need setup of Ubuntu 18.04

### Install and configure PostgreSQL server on your local machine:
```
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql postgres

postgres=# \password
Enter new password:
Enter it again:

postgres=# CREATE DATABASE your_custom_db_name;

postgres=# \q
sudo apt-get install python-psycopg2

sudo apt-get install libpq-dev
```


### In the project root create venv and install requirements with Make

```
export PYTHONPATH=$PYTHONPATH:/home/.../.../4m-fiels-service/fields-service
```
```
make dev-env
```
#### in case of failure:
```
. venv/bin/activate
pip install -r requirements.txt
```

### Run project

#### run in development mode
```
make dev-env
```

#### run in production mode
```
make prod-env
```


## Project team:
* **Lv-412.WebUI/Python team**:
    - @sikyrynskiy
    - @olya_petryshyn
    - @taraskonchak
    - @OlyaKh00
    - @ement06
    - @iPavliv
    - @Anastasia_Siromska
    - @romichh
