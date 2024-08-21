FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到容器中的 /app 目录
COPY . /app

# 安装 Python 包
RUN pip install flask modelscope
RUN pip install kantts -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html
RUN pip install tf_slim pyclipper shapely cosyvoice modelscope[audio] ttsfrd addict datasets oss2 simplejson sortedcontainers pytorch_wavelets tensorboardX
RUN python -m modelscope download --model damo/speech_sambert-hifigan_tts_zhiyan_emo_zh-cn_16k

# 暴露端口
EXPOSE 5000

# 启动 Flask 服务
CMD ["python", "__init__.py"]
