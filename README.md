# An example of clean architecture in Django

## Table of Contents

- [Clean architecture](#architecture)
- [Application functional](#functional)
- [Blog](#blog)
- [Technologies](#technologies)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [Shutdown](#shutdown)
- [Accessing the Application](#accessing-the-application)

## Architecture

1. Models - layer that represents the description of the data
2. Repository - layer that allows you to abstract away from a specific ORM or library by providing interfaces for interacting with a data source.
3. Specification - for various types of filtering and sorting, the repository accepts a list of specifications depending on the selected parameters.
4. Service - service layer allows you to combine the logic of working with the repository; this layer is abstracted from the library for working with a specific data model; repositories that support a set of interfaces are embedded in the service layer.
5. Interactor - with complex business logic using two or more actors, it allows to combine the work of various services.
6. Dependency container - allows you to collect all dependencies in one container from where controllers can work with different interactor
7. Data Transfer Object - an object that allows you to get rid of the infrastructure in this case, we do not depend on the framework and infrastructure objects such as request and model
8. View(controller) - layer allows you to receive HTTP requests, validate them using a serializer and pass them as an DTO object to an interactor that receives from the dependency container
9. Serializer - serializes data that comes in json format and further allows you to map to the DTO object
10. JWT Token - allows you to authenticate the user using a pair of refresh and access tokens
11. JSON - final data representation
12. Swagger - API documentation

## Functional

### Authentication application

1. Get JWT token with email and password credentials
2. Register new account, send email with activation token
3. Activate account using activation token
4. Reactivate token helps generate new activate token old token expired (1 day time of expiration)
5. Password reset if user forgot old password, generate password reset token and send via email
6. Change password if user has old credentials

## Blog 
Simple CRUD application

1. Category
2. Posts
3. Post comments

You can explore Swagger API docs to see all operations.


## Technologies

- [Postgres Official Documentation](https://www.postgresql.org/docs/)
Postgres is a powerful, open-source object-relational database system. In this project, it is used as the main data store. This service runs the latest version of Postgres, exposed on port 5432. It uses a volume to persist the database data.
- [PGAdmin Official Documentation](https://www.pgadmin.org/docs/)
PGAdmin is a popular management and development tool for Postgres. In this project, it is used to manage data in Postgres. This service runs the PGAdmin tool, exposed on port 3333.
- [Django Official Documentation](https://docs.djangoproject.com/)
Django is a high-level Python Web framework. In this project, it's used to create the backend service. This service builds the Django application and exposes it on port 8080.
- [Redis Official Documentation](https://redis.io/documentation)
Redis is an in-memory data structure store used as a database, cache, and message broker. In this project, it is used to manage tasks queue and as a cache for the Django application.
- [Redis Commander on GitHub](https://github.com/joeferner/redis-commander)
Redis Commander is a Redis management tool. In this project, it is used to provide a UI for managing Redis.
- [Celery Official Documentation](https://docs.celeryproject.org/en/stable/)
Celery is an asynchronous task queue/job queue based on distributed message passing. It's used in this project for running asynchronous tasks.
- [Celery Beat Official Documentation](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html)
Celery Beat is a Celery's built-in periodic task scheduler. It is used in this project to schedule periodic tasks.
- [Flower Official Documentation](https://flower.readthedocs.io/en/latest/)
Flower is a web-based tool for monitoring and administrating Celery clusters. In this project, it is used to monitor the Celery tasks and workers.
- [Gunicorn Official Documentation](https://gunicorn.org/)
Gunicorn, also known as 'Green Unicorn', is a Python WSGI HTTP server for UNIX. It's a pre-fork worker model, which means it forks multiple worker processes to handle incoming requests. In this project, Gunicorn is used as the HTTP server to serve the Django application.
- [Nginx Official Documentation](http://nginx.org/en/docs/)
Nginx is a powerful, high-performance, and flexible HTTP and reverse proxy server. It's also a mail proxy server. In this project, it's used as a reverse proxy to forward requests to Gunicorn server. This improves the overall performance as Nginx can handle multiple concurrent connections and static files more efficiently than Gunicorn. It also provides additional features like load balancing and HTTP caching.


## Prerequisites

1. Make sure you have Docker and Docker Compose installed on your system. You can check the installation instructions [here for Docker](https://docs.docker.com/get-docker/) and [here for Docker Compose](https://docs.docker.com/compose/install/).

## Setup

1. Clone the project:
```
git clone https://github.com/wspjoy2011/django_service.git
```
2. Navigate to the project directory:
```
cd django_service
```
3. Build and run the Docker containers:
```
docker-compose up -d --build
```

## Usage

1. The Swagger is accessible at `http://localhost:80`. Use next credentials email admin@example.com, password admin.
2. PGAdmin is accessible at `http://localhost:3333/`.
3. Redis Commander is accessible at `http://localhost:8081/`.
4. Flower (Celery monitoring tool) is accessible at `http://localhost:8082/`.

## Shutdown

1. To stop running containers and remove them:
```
docker-compose down
```

## Accessing the Application

* The Django application is accessible at `http://localhost:80/`
* The Redis Commander can be accessed at `http://localhost:8081/`
* Flower (the Celery monitoring tool) is accessible at `http://localhost:8082/`
* The PostgreSQL database can be accessed on `localhost` with port `5432`
* The PGAdmin tool can be accessed at `http://localhost:3333/`

Remember to replace `localhost` with the relevant IP address if you're not accessing these from the same machine where the services are running.

Please make sure to replace placeholders with your actual values in the `.env` file. Also, these instructions are subject to changes in the project, so always refer to the project's README or other documentation for the most accurate information.
