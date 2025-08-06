FROM python:3.10-slim

# Install Git (needed by DVC)
RUN apt-get update && apt-get install -y git

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /app

CMD ["dvc", "repro"]
