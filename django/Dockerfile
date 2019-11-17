# build, test, coverage
FROM python:3.8.0-slim-buster as build

WORKDIR /usr/src/app
COPY requirements*.txt ./
RUN pip install -r requirements.txt -r requirements-dev.txt

COPY . .

ENV INTEGRATION_TESTING 'True'
# TODO: Fix tests
# RUN pylint app &&\
# coverage run manage.py test --exclude-tag=integration
RUN python manage.py migrate
RUN python manage.py collectstatic --no-input
RUN coverage run manage.py test
RUN coverage html -d static/htmlcov
RUN echo "PyLint..." && (pylint_runner > pylint-report.txt || true)

# runtime
FROM python:3.8.0-alpine3.10
WORKDIR /usr/src/app

COPY requirements*.txt ./
RUN pip install -r requirements.txt

COPY . .
COPY --from=build /usr/src/app/staticfiles/ staticfiles/
COPY --from=build /usr/src/app/static/ static/

# ENV DJANGO_SECRET_KEY ...
ENV DJANGO_DEBUG False
ENV LOG_LEVEL 'INFO'
ENV LOG_JSON 'True'
ENV ADMIN_USER 'admin'
ENV ADMIN_EMAIL 'admin@example.com'
ENV ADMIN_PWD '123admin'
ENV CLEANUP_JOB_CRON '0 0 * * 0'
ENV CLEANUP_JOB_DAYS '7'

ENV DATA_DIR '/var/app'
EXPOSE 8000

ENTRYPOINT [ "/usr/src/app/docker-entrypoint.sh" ]
