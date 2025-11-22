FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Prepare flag for gitctf verification
RUN mkdir -p /var/ctf
COPY flag /var/ctf/flag
RUN chmod 400 /var/ctf/flag

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/static/uploads /app/static/wargame_attachments && chmod +x /app/docker-entrypoint.sh

EXPOSE 5000

ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "app:create_app()"]
