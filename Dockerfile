
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# 1. Copy the requirements file
COPY src/requirements.txt .

# 2. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the rest of the application code
COPY src/app.py .
COPY src/users.db . 

# Expose the port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]