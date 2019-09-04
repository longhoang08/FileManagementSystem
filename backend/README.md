## File management web app
### Start app with docker
#### Prerequisites
- Docker
- Docker-compose

#### Start app for development
- Copy .env.example => .env
- Edit mapping port, or environment if need
- Run `docker-compose up`
- Open http://localhost:{APP_PORT}/api 

#### Database Migrations

- Create new migration: `flask db init` (only once)
- Upgrade: `docker-compose exec app flask db upgrade`  
- Downgrade: `docker-compose exec app flask db downgrade`  

### Console commands

- To run application: `flask run`



#### Module structure
Each module is spitted by repository pattern
##### Repository Pattern
![alt text](https://i.imgur.com/cNUvEwZ.png "Repository Pattern")


##### Module folder structure
:file_folder: /api: define api url, request body, params  
:file_folder: /extensions: setup base configuration  
:file_folder: /helpers: define helper function (must be pure function)  
:file_folder: /models: define orm model  
:file_folder: /repositories: define repository to access data  
:file_folder: /services: handle business logic  
:file_folder: /tests: unit test

### 📙 Resource

#### Libraries
- Flask http://flask.pocoo.org/  
- Flask restplus: document api https://flask-restplus.readthedocs.io/en/stable/  
- Pytest: testing framework https://docs.pytest.org/en/latest/
- SqlAlchemy: orm http://flask-sqlalchemy.pocoo.org/2.3/
