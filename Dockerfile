# Use official Python image as base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pipx
RUN pipx install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files (optional for now)
# RUN python manage.py collectstatic --noinput

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
