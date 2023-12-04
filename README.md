# Passwords manager
## Description
The backend part of the service for managing and storing passwords for any services.  
After the containers are launched, the API documentation will be available at http://localhost/swagger/

## Launch
1. Clone project repository.
2. Install:
* <a href=https://www.docker.com/get-started>Docker</a>
* <a href=https://docs.docker.com/compose/install/>Docker-compose</a>
3. Create and fill in ".env":
<br><pre>cp .env.dist .env</pre><br>
```
DJANGO_SECRET_KEY=
TTL=30
PASSWORD_SECRET_KEY=ANY_SECRET_STRING

DB_ENGINE=django.db.backends.postgresql
DB_NAME=didenok
POSTGRES_USER=didenok
POSTGRES_PASSWORD=didenok
# Use "localhost" when running your project locally 
DB_HOST=db
DB_EXTERNAL_PORT=5432
DB_PORT=5432
```
4. To generate a DJANGO_SECRET_KEY, run the python script `create_dj_secret_key.py`. Add it to .env:
<br><pre>python create_dj_secret_key.py</pre><br>
5. Collect containers:
<br><pre>docker compose up -d --build</pre><br>

## Tests
1. Running tests:
<br><pre>pytest</pre><br>  

## API documentation
Web interface: http://localhost/swagger/

