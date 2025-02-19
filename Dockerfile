# Using Python 3.10 
FROM python:3.10

# Define work directory in container
WORKDIR /app

# Copy requirements file to container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files to container
COPY app /app
COPY properties /app/properties
COPY response /app/response

# Use port 3030 to access the API
EXPOSE 3030

# Init API
CMD ["uvicorn", "mock:app", "--host", "0.0.0.0", "--port", "3030","--reload"]

