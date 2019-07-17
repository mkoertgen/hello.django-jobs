# Development

## Prerequisites

- [Python 3.7+](https://www.python.org/downloads/)

## Checkout

```console
git clone <url>
pip install --user -r requirements.txt -r requirements-dev.txt
```

## Developing & Testing

As usual for a Django application, the list of task can be shown

```bash
# List of tasks
python manage.py
# Run development server
python manage.py runserver
```

Running tests & coverage

```console
coverage run manage.py test
coverage report -m
coverage html -d static/htmlcov
```

Include/exclude tests by tag, cf.: [Tagging Tests](https://docs.djangoproject.com/en/2.2/topics/testing/tools/#tagging-tests) (Django Documentation)

```console
python manage.py test --tag=unit --exclude-tag=integration
```
