FROM python:3.9-slim

WORKDIR /app

# Cài đặt các thư viện cần thiết
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Sao chép mã nguồn vào container
COPY . .

# Make port 8080 available (standard for GCP)
EXPOSE 8080

# Define environment variable for port (used by GCP)
ENV PORT=8080

# Run app using gunicorn when container launches
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app