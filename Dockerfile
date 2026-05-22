ARG PYTHON_VERSION=3.12-slim
FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

# Ensure build deps + setuptools/wheel are present, then install requirements
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl \
    && python -m pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && apt-get remove -y build-essential curl && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

COPY . /code/
COPY media/ /code/media/

RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "ecommerce.wsgi"]
