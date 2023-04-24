# Pull base image
FROM python:3.10.7-slim-bullseye

RUN pip install pipenv

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore

# Set work directory
WORKDIR /url_shorten

# Install dependencies
COPY Pipfile Pipfile.lock /url_shorten/
RUN pipenv install --system

# Copy project
COPY . /url_shorten/
