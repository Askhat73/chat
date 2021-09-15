# Pull base image
FROM python:3.9.1-alpine

# Set env vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

# Set work dir
WORKDIR /code

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev libffi-dev gcc python3-dev musl-dev
# install cryptography dependencies
RUN apk add libffi-dev

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/
