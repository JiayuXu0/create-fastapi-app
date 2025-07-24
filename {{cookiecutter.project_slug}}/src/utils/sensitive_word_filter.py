"""敏感词过滤工具模块

使用AhoCorasick算法进行高效的敏感词检测和过滤。
"""

import json

import ahocorasick

from log import logger
from settings.config import settings


class SensitiveWordFilter:
    """敏感词过滤器

    使用AhoCorasick算法实现高效的敏感词检测。
    """

    def __init__(self):
        """初始化敏感词过滤器"""
        self.automaton = None
        self.enabled = settings.ENABLE_SENSITIVE_WORD_FILTER
        self.response_message = settings.SENSITIVE_WORD_RESPONSE
        self._build_automaton()

    def _build_automaton(self) -> None:
        """构建AhoCorasick自动机

        将配置中的敏感词列表构建成自动机，用于快速匹配。
        """
        if not self.enabled:
            logger.info("敏感词过滤功能已禁用")
            return

        try:
            self.automaton = ahocorasick.Automaton()

            # 添加敏感词到自动机
            for idx, word in enumerate(settings.SENSITIVE_WORDS):
                if word.strip():  # 忽略空字符串
                    # 转换为小写进行匹配，提高匹配准确性
                    self.automaton.add_word(word.strip().lower(), (idx, word.strip()))

            # 构建自动机
            self.automaton.make_automaton()

            logger.info(
                f"敏感词过滤器初始化完成，共加载 {len(settings.SENSITIVE_WORDS)} 个敏感词"
            )

        except Exception as e:
            logger.error(f"构建敏感词自动机失败: {str(e)}")
            self.enabled = False

    def contains_sensitive_word(self, text: str) -> tuple[bool, str | None]:
        """检测文本是否包含敏感词

        Args:
            text: 待检测的文本

        Returns:
            Tuple[bool, Optional[str]]: (是否包含敏感词, 匹配到的敏感词)
        """
        if not self.enabled or not self.automaton or not text:
            return False, None

        try:
            # 转换为小写进行匹配
            text_lower = text.lower()

            # 使用自动机进行匹配
            for end_index, (
                _,
                original_word,
            ) in self.automaton.iter(text_lower):
                logger.warning(
                    f"检测到敏感词: {original_word} 在位置 {end_index - len(original_word) + 1}"
                )
                return True, original_word

            return False, None

        except Exception as e:
            logger.error(f"敏感词检测失败: {str(e)}")
            return False, None

    def filter_text(self, text: str) -> str:
        """过滤文本中的敏感词

        Args:
            text: 待过滤的文本

        Returns:
            str: 过滤后的文本，如果包含敏感词则返回提醒信息
        """
        if not text:
            return text

        contains_sensitive, matched_word = self.contains_sensitive_word(text)

        if contains_sensitive:
            logger.info(f"文本包含敏感词 '{matched_word}'，返回提醒信息")
            return self.response_message

        return text

    def filter_streaming_chunk(self, chunk: str) -> str | None:
        """过滤流式输出的数据块

        Args:
            chunk: 流式输出的数据块

        Returns:
            Optional[str]: 过滤后的数据块，如果包含敏感词则返回None表示阻止输出
        """
        if not chunk or not self.enabled:
            return chunk

        try:
            # 解析流式数据
            if chunk.startswith("data:"):
                json_content_str = chunk[len("data:") :].strip()
                if json_content_str and json_content_str != "[DONE]":
                    try:
                        event_data = json.loads(json_content_str)

                        # 检查不同类型的事件中的文本内容
                        text_to_check = ""

                        # 检查answer字段（通常包含AI回复内容）
                        if "answer" in event_data:
                            text_to_check += event_data["answer"]

                        # 检查其他可能包含文本的字段
                        if "text" in event_data:
                            text_to_check += event_data["text"]

                        if "content" in event_data:
                            text_to_check += str(event_data["content"])

                        # 如果有文本内容需要检查
                        if text_to_check:
                            (
                                contains_sensitive,
                                matched_word,
                            ) = self.contains_sensitive_word(text_to_check)

                            if contains_sensitive:
                                logger.warning(
                                    f"流式输出中检测到敏感词 '{matched_word}'，阻止输出"
                                )
                                # 返回None表示阻止输出
                                return None

                    except json.JSONDecodeError:
                        # 如果不是JSON格式，直接检查原始文本
                        contains_sensitive, matched_word = self.contains_sensitive_word(
                            json_content_str
                        )
                        if contains_sensitive:
                            logger.warning(
                                f"流式输出中检测到敏感词 '{matched_word}'，阻止输出"
                            )
                            return None

            return chunk

        except Exception as e:
            logger.error(f"过滤流式数据块失败: {str(e)}")
            return chunk

    def reload_sensitive_words(self) -> bool:
        """重新加载敏感词列表

        Returns:
            bool: 是否重新加载成功
        """
        try:
            logger.info("重新加载敏感词列表")
            self._build_automaton()
            return True
        except Exception as e:
            logger.error(f"重新加载敏感词列表失败: {str(e)}")
            return False


# 全局敏感词过滤器实例
sensitive_word_filter = SensitiveWordFilter()
