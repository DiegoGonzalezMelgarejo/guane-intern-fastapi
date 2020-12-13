
FROM python:3.8.5-slim as py

# Base
FROM py as base
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential python-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install fastapi uvicorn sqlalchemy mysql-connector-python bcrypt pyjwt pytest requests
WORKDIR /app
COPY app ./app/
COPY setup.py ./

# Dev
FROM base as develop
COPY --from=base / /


EXPOSE 8000

ENTRYPOINT ["uvicorn"]

# Production
FROM base as production
COPY --from=base / /
COPY gunicorn-config.py ./

RUN pip3 install --no-cache-dir . gunicorn

CMD exec gunicorn app.main:app -c gunicorn-config.py
