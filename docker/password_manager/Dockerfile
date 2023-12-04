FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt --no-cache-dir --no-input

COPY . /app
COPY ./docker/password_manager/entrypoint /app/entrypoint

RUN chmod +x /app/entrypoint
