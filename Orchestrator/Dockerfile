# Use a minimal, official base image
FROM python:3.9-slim

# Create a non-root user and set permissions
ARG APP_USER=appuser
ARG APP_UID=10001
ARG APP_GID=10001
RUN groupadd --gid $APP_GID $APP_USER && useradd --uid $APP_UID --gid $APP_GID -m $APP_USER
RUN mkdir -p /code && chown -R $APP_USER:$APP_GID /code

# Set the working directory
WORKDIR /code

# Copy only the requirements file first to leverage layer caching
COPY requirements.txt /code

# Install dependencies as root, then switch user
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application code and set ownership
COPY --chown=$APP_USER:$APP_GID . /code

# Expose the application port
EXPOSE 5000

# Switch to the non-root user
USER $APP_USER

# Run the application
CMD ["python", "app.py"]