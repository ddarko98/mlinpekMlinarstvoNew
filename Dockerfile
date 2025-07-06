ARG PYTHON_VERSION=3.12-slim

FROM python:${PYTHON_VERSION}

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /code/

# ✅ ADD THIS to copy your media files
COPY media/ /code/media/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port and set the command
EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "ecommerce.wsgi"]
