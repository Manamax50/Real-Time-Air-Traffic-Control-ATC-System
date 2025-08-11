# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/data && chmod a+rwx /app/data

ENV RABBITMQ_HOST=4.172.252.16
ENV RABBITMQ_PORT=5672
ENV RABBITMQ_USER=admin
ENV RABBITMQ_PASS=AdminPass123!
ENV SUPABASE_URL=https://rxyrnoobahmtvmbgdvlo.supabase.co
ENV SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4eXJub29iYWhtdHZtYmdkdmxvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzOTMzMzAsImV4cCI6MjA1ODk2OTMzMH0.u7DmI5KcRzPK8B8HMyfa2l-qFxKMQqPz_w8T6szQtvo

CMD ["python", "start_system.py"]