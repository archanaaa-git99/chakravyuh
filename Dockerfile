# Use a lightweight official Python image
FROM python:3.12-slim

# Set the working folder inside the container
WORKDIR /app

# Copy only requirements first (helps Docker cache installs faster on rebuilds)
COPY requirements.txt .

# Install all Python packages listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the project (backend/, docs/, tests/, etc.)
COPY . .

# Tell Docker this container listens on port 8000
EXPOSE 8000

# The command that runs when the container starts
# 0.0.0.0 (not 127.0.0.1) so it's reachable from outside the container
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]