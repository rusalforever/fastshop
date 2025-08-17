FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock README.md /app/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Тепер копіюємо весь проєкт (якщо є інші файли/папки)
COPY . /app

CMD ["sh", "ops/start-api.sh"]
