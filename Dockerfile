FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . /app

RUN chmod +x ops/start-api.sh

CMD ["sh", "ops/start-api.sh"]
