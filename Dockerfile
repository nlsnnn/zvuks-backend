FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./alembic.ini /code/alembic.ini
COPY ./app /code/app
COPY ./start.sh /code/start.sh

CMD ["sh", "/code/start.sh"]