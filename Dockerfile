FROM python:3.8.2-buster

WORKDIR /app

EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

RUN apt-get update && apt-get install -y gettext

# Update pip to the newest version
RUN pip install --upgrade pip
# Install pipenv
RUN pip install pipenv

# Copying Pipfile/Pipfile.lock
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# Install Python requirements
RUN pipenv install --deploy --system

COPY . /app

CMD gunicorn --pythonpath app config.wsgi:application --bind 0.0.0.0:8000
