# Use a lightweight official Python image
FROM python:3.12-slim

# Set the working folder inside the container
WORKDIR /app

# Copy only requirements first
COPY requirements.txt .

# Install all Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Create a fresh demo database and insert the fictional seed data
RUN rm -f /app/chakravyuh.db && python -m backend.seed.seed_data

# Tell Docker this container listens on port 8000
EXPOSE 8000

# Start the backend
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
