# build, test, coverage
FROM python:3.7.2 as build

WORKDIR /usr/src/app
COPY requirements*.txt ./
RUN pip install -r requirements.txt -r requirements-dev.txt

COPY . .

ENV INTEGRATION_TESTING 'True'
# TODO: Fix tests
# RUN pylint app &&\
# coverage run manage.py test --exclude-tag=integration
RUN coverage run manage.py test &&\
    coverage html -d static/htmlcov

# runtime
FROM python:3.7.2-alpine3.8
WORKDIR /usr/src/app

COPY requirements*.txt ./
RUN pip install -r requirements.txt

COPY . .
COPY --from=build /usr/src/app/static/ static/
RUN ./manage.py collectstatic --no-input

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
RUN mkdir -p ${DATA_DIR} && ./manage.py migrate
VOLUME ["/var/app"]

EXPOSE 8000

ENTRYPOINT [ "/usr/src/app/docker-entrypoint.sh" ]
