# Module 1 Homework: Docker & SQL

## Question 1. Understanding Docker images

Commands: 
* `docker run -it --rm python:3.13 bash`
* `pip --version`

**Solution**: `25.3`

## Question 2. Understanding Docker networking and docker-compose

- Containers running with docker compose run in the same network (homework-1_default in this case) and should talk to each other on internal ports. The host should use external port (5433 for postgres).
- To connect to postgres pgadmin can use the service name (db) or the container name (postgres).

**Solution** (multiple choice):
* postgres:5432
* db:5432