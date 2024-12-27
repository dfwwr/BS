FROM python:3.9

WORKDIR /app

# 安装 Edge WebDriver 依赖
RUN apt-get update && apt-get install -y \
    microsoft-edge-stable \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]