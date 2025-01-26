# Base stage for building dependencies
FROM python:3.10-slim AS builder

WORKDIR /app

# Install build dependencies in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies in a virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copy dependency file first to leverage caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Final stage for runtime
FROM python:3.10-slim AS runtime

WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /app/venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copy only necessary application files
COPY ./app /app/app
COPY entrypoint.sh /app/entrypoint.sh
COPY main.py /app/main.py

# Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Define entrypoint and default command
ENTRYPOINT ["bash"]
CMD ["entrypoint.sh"]