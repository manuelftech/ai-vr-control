FROM python:3.14-slim
ENV OPENAI_API_KEY="some_value"
ARG CONF_GROUP=groupconf
ARG CONF_USER=userconf
ARG PORT=5000
WORKDIR /src
COPY . /src
RUN apt-get update && \
    # Install tools for container debugging
    apt-get install curl -y && \
    # Create a non-root user and group
    groupadd $CONF_GROUP && \
    useradd $CONF_USER && \
    usermod -aG $CONF_GROUP $CONF_USER && \
    # Set permissions for the project directory
    mkdir -p /src && \
    chown -R $CONF_USER:$CONF_GROUP /src && \
    # Install Python dependencies
    pip install --no-cache-dir --upgrade -r /src/requirements.txt

EXPOSE $PORT
USER $CONF_USER
CMD ["python", "app.py"]