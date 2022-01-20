# fast-API-complete-version

# How to start this project:

  - To create you virtual env: python3 -m venv '<'name'>'

  - To activate your VENV: spurce '<'VENV-name'>'/bin/activate

  - Install fastapi: pip install fastapi[all]

  - To check packages installed: pip freeze
  
  - To Install Psycopg (it will make us "talk to our database"): pip install
    psycopg2-binary

## Server Note:

  To start your server: uvicorn '<'project-name'>':'<'path-operation-name'>' 

### Exemple:

  uvicorn app.main:app --reload (this will make that everytime you change something in your api you won't need to reload the server to check the change)

## Some Instructions to test:

  After doing this and checking the code, you can run your server and go to
route /docs to perform some requests, or you can use postman, or if you preferer
an easier way try to make the same requests on your terminal. But, if you just
want to try some requests on your terminal, but you don't know the commands,
just go to the route mentioned before and check the commands there ;)

  You can also try the route /redoc for a different format of documentation

## Database: 

The relational database management system used is PostgreSQL

  - First update your Ubunto packages before installing it: sudo apt update

  - To install PostgreSQL: sudo apt install postgresql

  - To set password: sudo passwd postgres

  - To start: sudo service postgresql start

  - To check status: sudo service postgresql status

  - To stop: sudo service postgresql stop

