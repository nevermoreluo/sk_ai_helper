import logging
from logging.handlers import TimedRotatingFileHandler
import os

# 创建日志目录
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# 设置日志配置
handler = TimedRotatingFileHandler(
    os.path.join(log_dir, 'app.log'),  # 日志文件路径
    when='midnight',                     # 每天午夜分割
    interval=1,                          # 每隔1天分割
    backupCount=1                       # 保留30个备份（最近30天的日志）
)


# 设置日志格式
formatter = logging.Formatter('%(asctime)s[%(levelname)s]: %(message)s')
handler.setFormatter(formatter)
handler.stream.reconfigure(encoding='utf-8')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.stream.reconfigure(encoding='utf-8')

# 创建logger并添加handler
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # 设置日志级别
logger.addHandler(handler)
logger.addHandler(stream_handler)
