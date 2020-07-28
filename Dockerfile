FROM python:3.8.2-buster

WORKDIR /app

# Update pip to the newest version
RUN pip install --upgrade pip
# Install pipenv
RUN pip install pipenv

# Copying Pipfile/Pipfile.lock
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# Install Python requirements
RUN pipenv install --deploy --system