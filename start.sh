#!/bin/bash

# 构建并启动容器
docker-compose up -d

# 等待后端启动
echo "Waiting for backend to start..."
sleep 10

# 执行数据库迁移
docker-compose exec backend python manage.py migrate

# 启动定时任务
docker-compose exec backend python manage.py crontab add

echo "Setup complete!"