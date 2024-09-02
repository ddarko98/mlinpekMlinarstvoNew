FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1 # Prevent Python from writing .pyc files to disk
ENV PYTHONUNBUFFERED 1 # Prevent Python from buffering stdout and stderr

COPY . /app/
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ecommerce.wsgi:application"]
