FROM python:alpine

RUN mkdir -p /opt/alp/backend
WORKDIR /opt/alp/backend

COPY . .

ADD . .

RUN pip install --upgrade pip

RUN \
 apk add --no-cache tzdata && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN python manage.py collectstatic --no-input


EXPOSE 8000
CMD gunicorn --chdir backend --bind :8000 backend.wsgi:application --workers 4 --timeout 300 --reload