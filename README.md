Example of [Starlette](https://www.starlette.io/) Q&A application made with [Piccolo ORM](https://www.piccolo-orm.com/) and [Piccolo Admin](https://github.com/piccolo-orm/piccolo_admin).

Open terminal and run:

```shell
virtualenv -p python3 envname
cd envname
source bin/activate
git clone https://github.com/sinisaos/starlette-piccolo-orm.git
cd starlette-piccolo-orm
pip install -r requirements.txt
sudo -i -u yourpostgresusername psql
CREATE DATABASE questions;
\q
touch .env
## put this in .env file
## DB_NAME="your db name"
## DB_USER="your db username"
## DB_PASSWORD="your db password"
## DB_HOST="your db host"
## DB_PORT=5432
## SECRET_KEY="your secret key"

## runing migrations for admin
piccolo migrations forwards user
piccolo migrations forwards session_auth
## runing migrations for site
piccolo migrations forwards questions
## create admin user
piccolo user create
uvicorn app:app --port 8000 --host 0.0.0.0 
```
After site is running log in as admin user and add categories, questions etc. For non admin user you can sign up and post content.
