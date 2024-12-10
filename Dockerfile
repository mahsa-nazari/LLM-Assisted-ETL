FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default Flask port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.dashboard.py
ENV FLASK_ENV=development
ENV DOCKER_ENV=true

# Allow users to override the default port and database URI
ARG PORT=5000
ENV PORT=$PORT

# Run the Flask app with the specified port
CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=$PORT"]

