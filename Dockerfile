FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc libpq-dev

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
