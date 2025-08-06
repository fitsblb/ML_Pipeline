FROM python:3.10-slim

WORKDIR /app

# Install dependencies first (for caching)
RUN pip install --no-cache-dir flask pandas scikit-learn numpy

# Copy model
COPY models/model.pkl ./models/model.pkl

# Copy serve script  
COPY serve/serve.py .

# Expose port for Flask
EXPOSE 8000

# Run the server
CMD ["python", "serve.py"]