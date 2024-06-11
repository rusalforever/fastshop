FROM python:3.11

WORKDIR /app

COPY pyproject.toml pyproject.toml

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . /app

RUN chmod +x ops/start-api.sh


CMD ["sh", "ops/start-api.sh"]
