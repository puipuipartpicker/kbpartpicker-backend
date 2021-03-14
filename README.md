# Backend and Scrapers for KBPartpicker

## Running the flask app on your local machine
### Setup Postgres
---
- Download Postgres
```
brew install postgres
```
- Create kbpartpicker database
```
createdb -h localhost -p 5432 -U {username} kbpartpicker
```
### Setup server
---
- Download the chromedriver that matches your chrome browser's version
https://chromedriver.chromium.org/downloads
- Install python dependencies (Be sure to use python 3)
```
poetry install
```
- Create a `.env` file inside the root directory with the following as its contents, and replace username with the username you used to create the database
```
export DB_USERNAME=kbpp
export DB_PASSWORD=password
export DB_HOST=db
export DB_NAME=kbpartpicker
export DB_PORT=5432
```
- `pg_ctl -D /usr/local/var/postgres start` to start postgres server
- `source config/.env` to export local environment variables.
- `python scrape.py` to populate the database.
- `python run.py` to start the server.
- `psql -U $USER -d kbpartpicker -h localhost -p 5432 -f config/kbpartpicker.sql` to update the database.
