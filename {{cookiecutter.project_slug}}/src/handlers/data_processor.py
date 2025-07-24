import json

from log import logger


class DataProcessor:
    """数据处理工具类 - 合并所有重复的数据处理逻辑"""

    @staticmethod
    def extract_workflow_data(chunks: list[str]) -> dict | None:
        """从数据块中提取workflow_finished事件数据 - 统一版本"""
        logger.info(f"开始从 {len(chunks)} 个数据块中提取workflow_finished事件")

        found_event_types = []

        # 从后往前查找，最新的事件在后面
        for i, chunk in enumerate(reversed(chunks)):
            if chunk.startswith("data:"):
                json_content_str = chunk[len("data:") :].strip()
                if json_content_str and json_content_str != "[DONE]":
                    try:
                        event_data = json.loads(json_content_str)
                        event_type = event_data.get("event")
                        if event_type:
                            found_event_types.append(event_type)

                        if event_type == "workflow_finished":
                            logger.info(
                                f"在数据块 {len(chunks) - 1 - i} 找到workflow_finished事件"
                            )
                            return event_data
                    except json.JSONDecodeError as e:
                        logger.warning(
                            f"解析数据块失败: {str(e)}, 内容: {json_content_str[:100]}..."
                        )
                        continue

        logger.warning(
            f"未找到workflow_finished事件。遍历了 {len(chunks)} 个数据块，"
            f"发现的事件类型: {found_event_types}"
        )
        return None

    @staticmethod
    def extract_text_from_chunks(chunks: list[str]) -> str:
        """从数据块中提取累积的文本内容"""
        accumulated_text = ""

        for chunk in chunks:
            if chunk.startswith("data:"):
                json_content_str = chunk[len("data:") :].strip()
                if json_content_str and json_content_str != "[DONE]":
                    try:
                        event_data = json.loads(json_content_str)
                        event_type = event_data.get("event")

                        # 从不同类型的事件中提取文本
                        if event_type == "text_chunk":
                            text = event_data.get("data", {}).get("text", "")
                            if text:
                                accumulated_text += text
                        elif event_type == "agent_message":
                            text = event_data.get("data", {}).get("answer", "")
                            if text:
                                accumulated_text += text
                        elif event_type == "message":
                            # 检查是否有输出内容
                            data = event_data.get("data", {})
                            if data.get("outputs"):
                                answer = data.get("outputs", {}).get("answer", "")
                                if answer:
                                    accumulated_text = answer  # 使用最终答案
                            elif data.get("answer"):
                                accumulated_text = data.get("answer")
                    except json.JSONDecodeError:
                        continue

        return accumulated_text.strip()

    @staticmethod
    def parse_chunk_event(chunk: str) -> dict | None:
        """解析数据块中的事件"""
        if not chunk.startswith("data:"):
            return None

        json_content_str = chunk[len("data:") :].strip()
        if not json_content_str or json_content_str == "[DONE]":
            return None

        try:
            return json.loads(json_content_str)
        except json.JSONDecodeError:
            return None

    @staticmethod
    def generate_title(query: str, answer: str) -> str:
        """生成标题"""
        if query and answer:
            return f"{query} - {answer}"[:50]
        elif query:
            return query[:50]
        elif answer:
            return answer[:50]
        else:
            return "New Chat"


# 全局实例
data_processor = DataProcessor()
