# Receipts Platform

## 12-Factor Micro Service Architecture

### Component Technologies

|aspect|technology|
|------|----------|
|Database|Postgres|
|ORM|SqlAlchemy|
|Models|Pydantic|
|REST server|FastAPI|
|Queue|RabbitMQ (pika)|
|Structured Event Logging|FluentD|

### 12 Factor App Methodology

This system attempts to fulfill the [12 factor app methodology](https://12factor.net/):

|Factor|Requirement|
|------|-----------|
Codebase|There should be exactly one codebase for a deployed service with the codebase being used for many deployments
Dependencies|All dependencies should be declared, with no implicit reliance on system tools or libraries
Config|Configuration that varies between deployments should be stored in the environment
Backing services|All backing services are treated as attached resources and attached and detached by the execution environment
Build, release, run|The delivery pipeline should strictly consist of build, release, run
Processes|Applications should be deployed as one or more stateless processes with persisted data stored on a backing service
Port binding|Self-contained services should make themselves available to other services by specified ports
Concurrency|Concurrency is advocated by scaling individual processes
Disposability|Fast startup and shutdown are advocated for a more robust and resilient system
Dev/Prod parity|All environments should be as similar as possible
Logs|Applications should produce logs as event streams and leave the execution environment to aggregate
Admin Processes|Any needed admin tasks should be kept in source control and packaged with the application

### Write/Read Model

The architecture splits the data persistence into a write model and a read model.  The write model is intended as the golden source of truth.  The read model is kept in sync with the write model using an event service (queue).  This allows the write model table structures to be optimized for fast insert and update, whereas by contrast the read model table structures are optimized for fast read.


## General Architecture

### (database) migrations

- yoyo migrations
- migration files @ codebase/model/migrations/write_model
- raw sql migrations => total control over schema
- seed data in code

-------------------------------------------------------------------------------

sudo snap install pgadmin4

## codium command prompts

### new service xxx

xxx = merchant_pos_callback

in python, create a new iss_bank_callback_service following the pattern for the existing merchant_pos_callback_service, as defined by the python source code files in folder codebase/services/merchant_pos_callback

update the docker-compose definition in file docker-compose.yml to add a new service merchant_pos_callback based on the existing entry for iss_bank_new_pmt


## general notes

# Development Notes

## docker, docker-swarm installation on linux (ubuntu 21.??)

sudo apt-get install docker-ce=5:20.10.8~3-0~ubuntu-hirsute docker-ce-cli=5:20.10.8~3-0~ubuntu-hirsute containerd.io

docker build -t restserver:latest .
docker run -dp 3000:3000 restserver:latest

docker logs $containerid -f

docker inspect --format "{{json .State.Health }}" 2aff56a67da2 | jq

docker cp <containerId>:/file/path/within/container /host/path/target

uvicorn test:app --reload

## Tech Stack

### language

python 3.?

### (python) web server - fastapi

[fastapi](https://github.com/tiangolo/fastapi) chosen over flask, due to promise of increased performance
=> docker image https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

postgresql docker image

https://hub.docker.com/_/postgres

ubuntu

sudo apt-get install libpq-dev

### logging - fluentd 

/fluentd/etc/fluent.conf

define <match fluent.**> to capture fluentd logs in top level is deprecated. Use <label @FLUENT_LOG> instead

### database - postgresql

db     | Error: Database is uninitialized and superuser password is not specified.
db     |        You must specify POSTGRES_PASSWORD to a non-empty value for the
db     |        superuser. For example, "-e POSTGRES_PASSWORD=password" on "docker run".


db    | The database cluster will be initialized with locale "en_US.utf8".
db    | The default database encoding has accordingly been set to "UTF8".
db    | The default text search configuration will be set to "english".

$ sudo su - postgres
$ psql -f /home/david/code/pydist/codebase/model/migrations/write_model/latest_base.sql 

# rabbitmq

not secured

management web console
http://localhost:15672/
guest, guest

## yoyo

yoyo apply --database postgresql://scott:tiger@localhost/db ./migrations