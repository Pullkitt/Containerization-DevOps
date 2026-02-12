# 1. Base Image: Use an official Python image (Version 3.10 or above)
# We use 'slim' to keep the image size smaller
FROM python:3.10-slim

# 2. Set a working directory inside the container
WORKDIR /app

# 3. Copying the application file from our computer to the container
COPY app.py .   

# 4. Install required dependencies
# The problem statement requires numpy to be installed via pip
RUN pip install numpy

# 5. Command to run the application when the container starts
CMD ["python", "app.py"]
