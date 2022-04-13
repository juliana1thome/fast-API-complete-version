# Main Idea:

This project is suppose to be an "Social Media". But, let's be honest it is an
API with no front-end code ¯\_(ツ)_/¯ because I just want to practice some
back-end (◕‿◕)♡ Therefore, I gave this brillian name, Fake Social Media (￢‿￢)

# How to start this project:

  - To create you virtual env: python3 -m venv '<'name'>'

  - To activate your VENV: source '<'VENV-name'>'/bin/activate

  - Install fastapi: pip install fastapi[all]

  - To check packages installed: pip freeze
  
  - To Install Psycopg (it will make us "talk to our database"): pip install
    psycopg2-binary

## Server Note:

  To start your server: uvicorn '<'project-name'>':'<'path-operation-name'>' 

### Example:

  uvicorn app.main:app --reload (this will make that everytime you change something in your api you won't need to reload the server to check the change)

## Some Instructions to test it out:

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

## ENV:
  
  - To set a ENV variable type: export MY_ENV_VARIABLE='whatever:value'

  - To check all yours ENV variables: printenv

  - To check just one ENV variables: echo $MY_ENV_VARIABLE

## ORM:

  - The ORM used in this project is SQLAlchemy

  - Version used: 1.4

  - To install: pip install sqlalchemy

  - For more information to understand how this was used in the project check
    this [link](https://fastapi.tiangolo.com/advanced/async-sql-databases/?h=sqlalche#import-and-set-up-sqlalchemy)

## Password Hashing:

  - To install passlib but with Bcrypt as the algorithm used: pip install passlib[bcrypt]

## JWT Token:

  - To install python-jose to generate and verify JWT tokens: pip install
    python-jose[cryptography]

## Database Migration Tool (Alembic):

  - Link for the instructions on how to setup the migration environment:
    https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment

  - To install alembic 1.7.7: pip install alembic 

  - For alembic help: alembic --help

  - To create an alembic directory: alembic init (the name that you want for this)
    -> it will create both alembic directory and an alembic ini file

  - To create a new revision (what tracks the changes made on the DB(same idea as
    commit used on git)): alembic revision -m "The message that you want to add"

  - Note: the alembic revision will have an version file where you can add the
    logic to upgrade or dowgrade the table in question. To know how to perform any
    logic on this file visit this website:
    https://alembic.sqlalchemy.org/en/latest/api/ddl.html#module-alembic.ddl.mysql 

  - To see which version you are: alembic current

  - To upgrade your alembic version: alembic upgrade (the version of the revision
    that you want) -> when you do this it will create a table that will allow you to
    keep check on the revisions

  - To downgrade your alembic version: alembic downgrade -n (n is the numbers of
    revisions you want to go under) or you can use just the revision

  - To allow alembic to do everything for you just by getting your models from
    sqlalchemy type: alembic revision --autogenerate -m "message"

## Running in an isolated environment:

  - Note: This application is missing the container for the PostgreSQL server to be
    completely running in an isolated environment.

  - But to run the app only in a container, you first must run this: make build

  - And after, run this: make run
