FROM node:16-slim

WORKDIR /app

# 设置淘宝 npm 镜像源
RUN npm config set registry https://registry.npmmirror.com

# 安装依赖前复制 package.json 和 package-lock.json (如果存在)
COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]