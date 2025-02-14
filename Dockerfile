# Python runtime parent image
FROM python:3.11.2-slim

# Set the working directory
WORKDIR /app

# Copy current directory contents into the container at /app
COPY . /app

# Install python packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the application when the container launches
CMD ["python", "app.py"]
