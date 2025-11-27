FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        chromium \
        chromium-driver \
        fonts-liberation \
        libasound2 \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libdrm2 \
        libgbm1 \
        libnspr4 \
        libnss3 \
        libu2f-udev \
        libvulkan1 \
        libx11-6 \
        libx11-xcb1 \
        libxcb1 \
        libxcomposite1 \
        libxdamage1 \
        libxext6 \
        libxfixes3 \
        libxkbcommon0 \
        libxrandr2 \
        libxss1 \
        libxtst6 \
        wget \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

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
