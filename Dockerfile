FROM python:3.11-slim

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
COPY . /app/
CMD alembic upgrade head  && gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8001 --forwarded-allow-ips '*'

