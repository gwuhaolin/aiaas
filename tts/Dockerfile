# 使用官方的 Python 3.8 镜像作为基础镜像
FROM python:3.8-slim-buster

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到容器中的 /app 目录
COPY . /app

# 安装所需的依赖包
RUN apt-get update && apt-get install -y \
    build-essential \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 包
RUN pip install --no-cache-dir \
    torch \
    flask modelscope

# 暴露端口
EXPOSE 5000

# 启动 Flask 服务
CMD ["python", "__init__.py"]
