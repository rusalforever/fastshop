FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry config virtualenvs.in-project false

RUN poetry install --only=main --no-interaction --no-ansi --no-root

COPY . /app

CMD ["sh", "ops/start-api.sh"]