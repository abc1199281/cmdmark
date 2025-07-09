FROM python:3.12-slim

WORKDIR /app

# 1. Copy only the dependency definition files first.
COPY pyproject.toml poetry.lock* ./

# 2. Install dependencies. This layer will be cached if these files don't change.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install .[test]

# 3. Copy the rest of the source code.
COPY . .

CMD ["pytest", "-q"]
