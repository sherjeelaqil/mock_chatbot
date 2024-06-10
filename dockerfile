FROM python:3.12-slim

WORKDIR /app

# Copying the application folder inside the container
COPY . /app
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN useradd -m myuser
RUN mkdir -p /app/logs
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install supervisor

EXPOSE 8000
EXPOSE 8080

# Set permissions
RUN chown -R myuser:myuser /app/logs
RUN chown -R myuser:myuser /app

# Switching to user
USER myuser

# Command to run Supervisor with specified config file
CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
