FROM nvidia/cuda:12.6.0-cudnn-runtime-ubuntu22.04

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到容器中的 /app 目录
COPY . /app

# 安装 Python 包
RUN pip3 install --no-cache-dir \
    torch \
    flask modelscope

# 暴露端口
EXPOSE 5000

# 启动 Flask 服务
CMD ["python3", "__init__.py"]
