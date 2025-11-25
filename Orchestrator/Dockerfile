FROM python:3.12-slim
ARG CONF_GROUP=conf
ARG CONF_USER=conf
ARG PORT=5000
WORKDIR /src
COPY . /src
RUN apt-get update && \
    # Install tools for container debugging and diagnostics
    apt-get install curl -y && \
    # Create a new system group and assign a user
    groupadd $CONF_GROUP \
    usermod -aG $CONF_GROUP $CONF_USER \
    mkdir /src \
    # Set permissions for the project directory
    chown -R $CONF_USER:$CONF_GROUP /src \
    # Install Python dependencies
    pip install --no-cache-dir --upgrade -r /src/requirements.txt

EXPOSE $PORT
USER $CONF_USER
CMD ["python", "app.py"]