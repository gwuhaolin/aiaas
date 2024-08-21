FROM pytorch/pytorch:2.4.0-cuda11.8-cudnn9-runtime

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到容器中的 /app 目录
COPY . /app

# 安装 Python 包
RUN pip install flask modelscope

# 暴露端口
EXPOSE 5000

# 启动 Flask 服务
CMD ["python", "__init__.py"]
