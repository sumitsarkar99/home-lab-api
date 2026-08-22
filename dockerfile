FROM python:3.14-slim AS builder

WORKDIR /code

RUN pip install --no-cache-dir --upgrade pip

# Copy only what is needed for installing dependencies
COPY pyproject.toml .

# Install dependencies into a wheels directory
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /code/wheels -e ".[dev]"

FROM python:3.14-slim AS runtime

WORKDIR /code

# Copy wheels from builder stage
COPY --from=builder /code/wheels /images/wheels
COPY pyproject.toml .

# Install the wheels
RUN pip install --no-cache-dir /images/wheels/* && rm -rf /images/wheels

# Copy application files
COPY ./app /code/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

