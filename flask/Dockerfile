# --- build, test, coverage
FROM python:3.8.0-slim-buster as build

WORKDIR /usr/src/app
COPY requirements*.txt ./
RUN pip install -r requirements.txt -r requirements-dev.txt

COPY . .
RUN flask db upgrade
# TODO: breaks with `coverage.misc.CoverageException: No data to report.`
#RUN nosetests --exe -vv -all-modules --collect-only
# --cover-xml for sonar
RUN nosetests --exe --cover-package=. --with-xunit --with-coverage --cover-tests --cover-inclusive\
    --cover-html --cover-html-dir application/static/cover

# TODO: raise test coverage & enable quality gate
#  --cover-min-percentage=80
#RUN echo "PyLint..." && (pylint_runner > pylint.txt || true)
RUN echo "PyLint..." && (pylint jobs > pylint.json || true)
RUN pylint-json2html -f jsonextended -o static/lint/pylint.html pylint.json

# --- analyze
# FROM newtmitch/sonar-scanner:4.0.0-alpine as analyze
# ARG SONAR_URL=https://sonarcloud.io
# ARG SONAR_LOGIN=
# ARG SONAR_ORGANIZATION=tracto-technik
# WORKDIR /usr/src/app
# COPY --from=test /usr/src/app/ .
# RUN if [[ ${SONAR_LOGIN:+0} ]]; then\
#   sonar-scanner -Dsonar.projectBaseDir=. -Dsonar.host.url=${SONAR_URL} -Dsonar.login=${SONAR_LOGIN} -Dsonar.organization=${SONAR_ORGANIZATION};\
#   fi

# --- final
FROM python:3.8.0-alpine3.10
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
COPY --from=build /usr/src/app/application/static/ application/static/

# cf.: https://askubuntu.com/questions/117359/how-do-i-change-the-timezone-to-utc
ENV TZ UTC

ENV FLASK_DEBUG '0'
ENV LOG_LEVEL 'INFO'
ENV LOG_JSON 'True'
ENV CLEANUP_JOB_CRON '0 0 * * 0'
ENV CLEANUP_JOB_DAYS '7'
ENV DATA_DIR '/var/app'
EXPOSE 5000

ENTRYPOINT [ "/usr/src/app/docker-entrypoint.sh" ]
