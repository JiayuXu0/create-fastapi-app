import json
import time

from fastapi.responses import StreamingResponse

from log import logger
from schemas.base import Success
from utils.sensitive_word_filter import sensitive_word_filter


class SensitiveFilterHandler:
    """统一的敏感词处理器"""

    def __init__(self):
        self.filter = sensitive_word_filter

    def check_input(self, text: str) -> tuple[bool, str | None]:
        """检查输入文本是否包含敏感词

        Returns:
            Tuple[bool, Optional[str]]: (是否包含敏感词, 匹配的敏感词)
        """
        return self.filter.contains_sensitive_word(text)

    async def handle_sensitive_input_stream(self, matched_word: str, query: str):
        """处理包含敏感词的流式请求"""
        logger.warning(f"用户输入包含敏感词 '{matched_word}': {query[:100]}")

        async def sensitive_word_response():
            # 发送敏感词提醒
            error_event = {
                "event": "error",
                "answer": self.filter.response_message,
            }
            yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
            # 发送结束信号
            yield "data: [DONE]\n\n"

        return StreamingResponse(
            sensitive_word_response(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
            },
        )

    def handle_sensitive_input_sync(self, matched_word: str, query: str):
        """处理包含敏感词的同步请求"""
        logger.warning(f"用户输入包含敏感词 '{matched_word}': {query[:100]}")
        return Success(
            data={
                "status": "blocked",
                "message": self.filter.response_message,
                "code": "SENSITIVE_CONTENT_DETECTED",
            }
        )

    def filter_chunk(self, chunk: str) -> str | None:
        """过滤数据块中的敏感词"""
        return self.filter.filter_streaming_chunk(chunk)

    def create_sensitive_response_data(self, event_data: dict | None = None) -> dict:
        """创建敏感词响应数据"""
        return {
            "event": "workflow_finished",
            "data": {"outputs": {"answer": self.filter.response_message}},
            "message_id": event_data.get("message_id") if event_data else "",
            "workflow_run_id": (
                event_data.get("workflow_run_id") if event_data else ""
            ),
            "created_at": int(time.time()),
        }

    def create_sensitive_stream_message(self, event_data: dict | None = None) -> dict:
        """创建敏感词流式消息"""
        return {
            "event": "error",
            "message_id": event_data.get("message_id") if event_data else "",
            "conversation_id": (
                event_data.get("conversation_id") if event_data else ""
            ),
            "answer": self.filter.response_message,
        }


# 全局实例
sensitive_filter_handler = SensitiveFilterHandler()
