import os
import sys

from loguru import logger as loguru_logger

from settings import settings


class LoggingConfig:
    """统一日志配置管理"""

    def __init__(self) -> None:
        self.debug = settings.DEBUG
        self.level = "DEBUG" if self.debug else "INFO"
        self.log_dir = "logs"
        self.ensure_log_dir()

    def ensure_log_dir(self):
        """确保日志目录存在"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir, exist_ok=True)

    def get_log_format(self):
        """获取统一的日志格式"""
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

    def get_file_format(self):
        """获取文件日志格式（无颜色）"""
        return (
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{name}:{function}:{line} | "
            "{message}"
        )

    def setup_logger(self):
        """配置日志输出"""
        # 清除默认处理器
        loguru_logger.remove()

        # 控制台输出（带颜色）
        loguru_logger.add(
            sink=sys.stdout,
            level=self.level,
            format=self.get_log_format(),
            colorize=True,
            backtrace=True,
            diagnose=True,
        )

        # 文件输出 - 所有级别日志
        loguru_logger.add(
            sink=f"{self.log_dir}/backend_{{time:YYYY-MM-DD}}.log",
            level="DEBUG",
            format=self.get_file_format(),
            rotation="100 MB",
            retention="30 days",
            compression="zip",
            encoding="utf-8",
            backtrace=True,
            diagnose=True,
        )

        # 错误日志单独文件
        loguru_logger.add(
            sink=f"{self.log_dir}/backend_error_{{time:YYYY-MM-DD}}.log",
            level="ERROR",
            format=self.get_file_format(),
            rotation="50 MB",
            retention="90 days",
            compression="zip",
            encoding="utf-8",
            backtrace=True,
            diagnose=True,
        )

        # 为所有日志添加默认上下文
        # 注意：这里重新绑定会创建新的logger实例

        # 记录日志系统启动
        loguru_logger.info("日志系统已启动")

        return loguru_logger


# 全局日志配置实例
logging_config = LoggingConfig()
logger = logging_config.setup_logger()
