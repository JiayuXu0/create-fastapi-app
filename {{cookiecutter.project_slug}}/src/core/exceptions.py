from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from starlette.responses import Response
from tortoise.exceptions import DoesNotExist, IntegrityError

from settings.config import settings


class SettingNotFound(Exception):
    pass


async def DoesNotExistHandle(req: Request, exc: DoesNotExist) -> JSONResponse:
    # 根据环境决定错误信息详细程度
    if settings.DEBUG:
        msg = f"Object not found: {exc}, query_params: {req.query_params}"
    else:
        msg = "请求的资源不存在"

    content = dict(code=404, msg=msg)
    return JSONResponse(content=content, status_code=404)


async def HttpExcHandle(request: Request, exc: HTTPException):
    if exc.status_code == 401 and exc.headers and "WWW-Authenticate" in exc.headers:
        return Response(status_code=exc.status_code, headers=exc.headers)
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "msg": exc.detail, "data": None},
    )


async def IntegrityHandle(request: Request, exc: IntegrityError):
    # 根据环境决定错误信息详细程度
    if settings.DEBUG:
        msg = f"IntegrityError: {exc}"
    else:
        msg = "数据完整性错误，请检查输入数据"

    content = dict(code=500, msg=msg)
    return JSONResponse(content=content, status_code=500)


async def RequestValidationHandle(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    # 根据环境决定错误信息详细程度
    if settings.DEBUG:
        msg = f"RequestValidationError: {exc}"
    else:
        msg = "请求参数验证失败，请检查输入格式"

    content = dict(code=422, msg=msg)
    return JSONResponse(content=content, status_code=422)


async def ResponseValidationHandle(
    _: Request, exc: ResponseValidationError
) -> JSONResponse:
    # 根据环境决定错误信息详细程度
    if settings.DEBUG:
        msg = f"ResponseValidationError: {exc}"
    else:
        msg = "服务器响应格式错误"

    content = dict(code=500, msg=msg)
    return JSONResponse(content=content, status_code=500)
