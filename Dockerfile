FROM python:3.11

WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN pip install poetry \
    && poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-root

COPY . /app

RUN chmod +x ops/start-api.sh

CMD ["sh", "ops/start-api.sh"]
