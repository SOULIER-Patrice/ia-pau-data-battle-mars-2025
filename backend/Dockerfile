FROM python:3.13

# Set environment variables
ENV APP_HOME /app

# Set working directory
WORKDIR $APP_HOME

# Copy application code
COPY . ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the backend port
EXPOSE 8000

# Run the backend
CMD ["./entrypoint.sh"]