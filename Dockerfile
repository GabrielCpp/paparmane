# Use an official Python runtime as a parent image
FROM python:3.12.1-bookworm as build

# Set the working directory in the container to /app
WORKDIR /app

#RUN apt-get update && apt install build-essential
RUN pip install poetry

# Install project dependencies
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create true \
  && poetry config virtualenvs.in-project true \
  && poetry install --no-interaction --no-ansi

COPY willy_gaby /app/willy_gaby
COPY README.md /app/README.md
COPY app.py app.py
COPY uvicorn_entry.py uvicorn_entry.py
RUN poetry install --only-root

FROM python:3.12.1-slim-bookworm as release
WORKDIR /app
USER nobody

COPY models/ /app/models/
COPY --from=build /app /app
ENV PATH="/app/.venv/bin:$PATH"
ENV PORT=80
CMD ["python", "uvicorn_entry.py"]