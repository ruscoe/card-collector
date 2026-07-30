FROM python:3.12-slim

WORKDIR /app

COPY api/requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY api /app/api

EXPOSE 5000
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "api.app"]
