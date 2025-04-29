# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and app into container
COPY requirements.txt requirements.txt
COPY app.py app.py

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask's default port
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]

