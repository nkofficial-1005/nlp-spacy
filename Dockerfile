# Use an official Python runtime as a parent image (Python 3.9)
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Create a cache directory that is writable
RUN mkdir -p /app/.cache/huggingface/hub

# Set the environment variable to point to the writable cache directory
ENV TRANSFORMERS_CACHE=/app/.cache

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download the spaCy English model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Expose port 80 for the container
EXPOSE 80

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]