import os
import sys

from settings.config import settings

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

TORTOISE_ORM = settings.TORTOISE_ORM
