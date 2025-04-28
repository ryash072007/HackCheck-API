# Use the official PostgreSQL image as the base
FROM postgres:latest

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . .

# Make sure the entrypoint script is executable
RUN chmod +x docker-entrypoint.sh

# Set the entrypoint to use the PostgreSQL entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]

# Default command when container starts
CMD ["postgres"]

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Set environment variables for PostgreSQL
ENV POSTGRES_PASSWORD=root
ENV POSTGRES_DB=hackcheck