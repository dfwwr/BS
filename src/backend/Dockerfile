FROM python:3.9-slim

WORKDIR /app

# 安装 Chromium 和其他依赖
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    chromium-driver \
    cron \
    && rm -rf /var/lib/apt/lists/*

# 设置 Chromium 和 ChromeDriver 环境变量
ENV CHROME_OPTIONS="--headless --no-sandbox --disable-dev-shm-usage"
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制源代码
COPY . /app/

EXPOSE 8000
