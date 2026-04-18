# Use a lightweight Python image
FROM python:3.9-slim

# Install Nmap and other system dependencies
RUN apt-get update && apt-get install -y nmap && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files
COPY . .

# Expose the port Render will use
EXPOSE 10000

# Start the application using Gunicorn (Better for cloud than Flask's built-in server)
CMD ["gunicorn", "--timeout", "100", "app:app"]