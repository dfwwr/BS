#!/bin/bash

# 加载镜像
docker load < bs-frontend.tar
docker load < bs-backend.tar

# 启动服务
docker compose up -d 