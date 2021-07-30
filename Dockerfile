FROM python:3-alpine

RUN mkdir -p /usr/src/flaskapp

WORKDIR /usr/src/flaskapp

# Copy files from project folder to WORKDIR
COPY . .

# install psycopg2 dependencies (this is required)
RUN apk update
RUN apk add build-base
RUN apk add postgresql-dev gcc python3-dev musl-dev

# install app dependencies
RUN python3 -m pip install -r requirements.txt --no-cache-dir

# Details about the db service in docker-compose.yml file
ENV APP_DATABASE_URL='postgresql://flaskapp:root@flaskdb:5432/todo_app'

ENV PORT=5000

CMD ["python3.9", "app.py"]
