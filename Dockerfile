# Base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1




# Install pipenv and system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && pip install pipenv

# Set work directory
WORKDIR /code


# Copy Pipenv files
COPY Pipfile Pipfile.lock /code/

# Install packages via pipenv
RUN pipenv install --deploy --system
# Copy project
COPY . /code/

# Set environment so pipenv virtualenv is used
ENV PATH="/root/.local/share/virtualenvs/code-*/bin:$PATH"

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

