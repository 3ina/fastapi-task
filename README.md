
# Task for top company

This repository contains the task for the  Top company  job interview.


## Run Locally

Clone the project

```bash
  https://github.com/3ina/fastapi-task
```

Go to the project directory

```bash
  cd ./fastapi-task
```

create .env file

```bash
  cp .env.example .env
```

Start the server

```bash
  docker compose -f docker-compose.dev.yml up -d --build
```


Run tests

```bash
  docker compose -f docker-compose.dev.yml exec api uv run pytest -v
```


## Authors

- [@sina roydel](https://www.github.com/3ina)


