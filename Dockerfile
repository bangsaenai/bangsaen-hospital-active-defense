# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# ติดตั้ง dependencies
RUN pip install --no-cache-dir fastapi uvicorn

# ก๊อปปี้สคริปต์ KMS Server เข้า Container
COPY builder/cloud_kms_server.py /app/builder/cloud_kms_server.py

EXPOSE 8080

# สั่งรัน uvicorn บน Port 8080 ตามมาตรฐาน GCP Cloud Run
CMD ["python", "-m", "uvicorn", "builder.cloud_kms_server:app", "--host", "0.0.0.0", "--port", "8080"]