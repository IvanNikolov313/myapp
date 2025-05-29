FROM python:3.11-slim

# Add bash and system utilities
RUN apt-get update && apt-get install -y bash curl

# Setup work directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Fix for missing CLI tools (alembic, etc.)
ENV PATH="/root/.local/bin:$PATH"

# Copy the app code
COPY ./app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
