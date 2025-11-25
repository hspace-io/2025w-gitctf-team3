FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc6-dev && \
    rm -rf /var/lib/apt/lists/*

# Prepare flag for gitctf verification and challenge runtime
RUN mkdir -p /var/ctf
COPY flag /var/ctf/flag
RUN chmod 400 /var/ctf/flag
COPY flag /flag.txt
RUN chmod 400 /flag.txt && chown root:root /flag.txt

COPY readflag.c /tmp/readflag.c
RUN gcc /tmp/readflag.c -o /readflag && chmod 4555 /readflag && rm /tmp/readflag.c

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
