FROM python:3.9-slim

# Set the working directory
WORKDIR /smsapp

# Copy the current directory contents into the container at /smsapp/
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /smsapp/
COPY . .

# Expose port 5001 to the outside world
EXPOSE 5001


# Run app.py when the container launches
CMD ["python", "app.py"]

