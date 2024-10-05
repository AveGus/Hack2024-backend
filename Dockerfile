FROM python:3.12

RUN apt-get update \
	&& apt-get install -y --no-install-recommends

RUN pip install poetry
USER root
WORKDIR /app

COPY src .
COPY pyproject.toml .
COPY poetry.lock .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

RUN poetry config virtualenvs.create false --local
RUN poetry install

CMD ["python3", "-m", "uvicorn", "main:app"]