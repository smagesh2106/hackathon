
# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/tmp

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --root-user-action=ignore  --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install --root-user-action=ignore  gunicorn

# Copy the rest of the application code into the container at /usr/src/app
COPY . .

RUN make all

# Compile all the source files
#RUN python -m compileall .

#Change to compiled code dir.
WORKDIR /app

RUN cp -r /usr/src/tmp/build/*  .
RUN rm -rf /usr/src/tmp
# Make port 80 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run app.py when the container launches
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "main:app"]
