# Dockerfile (backend)
FROM python:3.10.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container, including 'static' directory
COPY . /app

# Ensure the 'static' directory exists by copying it explicitly
COPY ./app/static /app/static

# Expose the port the app runs on
EXPOSE 8080

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
