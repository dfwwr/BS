FROM python:3.9-slim

WORKDIR /app

# 添加 Microsoft Edge 源
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add - \
    && echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list

# 安装 Microsoft Edge 和其他依赖
RUN apt-get update && apt-get install -y \
    microsoft-edge-stable \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 下载匹配版本的 Edge WebDriver
RUN EDGE_VERSION=$(microsoft-edge --version | cut -d ' ' -f 3) \
    && wget -q "https://msedgedriver.azureedge.net/${EDGE_VERSION}/edgedriver_linux64.zip" \
    && unzip edgedriver_linux64.zip \
    && mv msedgedriver /usr/local/bin/ \
    && rm edgedriver_linux64.zip

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制整个后端目录
COPY . /app/

EXPOSE 8000

CMD ["python", "PriceMatch/manage.py", "runserver", "0.0.0.0:8000"]