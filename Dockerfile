# Use the official Python image with version 3.11.0
FROM python:3.11.0-slim-buster

# Install necessary system dependencies including pdflatex
RUN apt-get update && apt-get install -y \
  texlive-latex-base \
  texlive-latex-extra \
  texlive-fonts-recommended \
  texlive-fonts-extra \
  texlive-xetex \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the /src contents into the container at /app
COPY ./src .

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the Flask application
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
