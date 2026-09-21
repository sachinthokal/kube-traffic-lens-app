FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

# Pass App Version at the time of Build
ARG APP_VERSION=v1.0.0
ENV APP_VERSION=$APP_VERSION

CMD ["python", "app.py"]