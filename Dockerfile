FROM python:3.11-slim

# 1. Create a non-root user with a specific UID
#    '-m' creates a home directory for them
RUN useradd -m -u 1000 dockeruser

# Set working directory
WORKDIR /app

# 2. Copy files and transfer ownership to 'dockeruser'
COPY --chown=dockeruser:dockeruser src/requirements.txt .

# Install dependencies (as root, which is fine for system libraries)
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the app code and DB, verifying ownership
COPY --chown=dockeruser:dockeruser app.py .
COPY --chown=dockeruser:dockeruser users.db .

# 4. CRITICAL: Switch to the non-root user
USER dockeruser

# Expose port and run
EXPOSE 5000
CMD ["python", "app.py"]