# Backend and Scrapers for KBPartpicker
## Setup Postgres
---
- Download Postgres
```
brew install postgres
```
- Create kbpartpicker database
```
createdb -h localhost -p 5432 -U {username} kbpartpicker
```
## Setup server
---
- Download the chromedriver that matches your chrome browser's version
https://chromedriver.chromium.org/downloads
- Install python dependencies (Be sure to use python 3)
```
poetry install
```
- Create a `.env` file inside the `config` directory with the following as its contents, and replace username with the username you used to create the database
```
DB_USERNAME=kbpp
DB_PASSWORD=password
DB_HOST=db
DB_NAME=kbpartpicker
DB_PORT=5432
DATABASE_URL=postgres+psycopg2://kbpp:password@db:5432/kbpartpicker
export DATABASE_URL=postgres+psycopg2://kbpp:password@db:5432/kbpartpicker
export MODE=dev
export TEST=1
```
- Run `pg_ctl -D /usr/local/var/postgres start` to start postgres server
- Run `source config/.env` to export local environment variables.
- Run `python scrape.py` to populate the database.
- Run `python run.py` to start the server.
- Run `psql -U $USER -d kbpartpicker -h localhost -p 5432 -f config/kbpartpicker.sql` to update the database.
