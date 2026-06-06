from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.responses import ERROR_RESPONSES_REGISTRY

EXCEPTION_MAP = {}

EXCEPTION_MAP = {}

for code, schema_cls in ERROR_RESPONSES_REGISTRY.items():
    try:
        instance = schema_cls()
        error_cls = instance.error_cls
        if error_cls and error_cls is not Exception:
            EXCEPTION_MAP[error_cls] = code
    except Exception as e:
        print(f"Warning: Could not get error_cls from {schema_cls}: {e}")
        if hasattr(schema_cls, '_error_cls'):
            error_cls = getattr(schema_cls, '_error_cls', None)
            if error_cls and error_cls is not Exception:
                EXCEPTION_MAP[error_cls] = code


async def exception_handler(_: Request, exc: Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    for error_cls, code in EXCEPTION_MAP.items():
        if isinstance(exc, error_cls):
            status_code = code
            break

    message = getattr(exc, 'message', str(exc))
    detail = getattr(exc, 'detail', None)

    return JSONResponse(
        status_code=status_code,
        content={
            'message': message,
            'detail': detail,
        }
    )


async def exception_handler(_: Request, exc: Exception):
    status_code = 500

    for error_cls, code in EXCEPTION_MAP.items():
        if isinstance(exc, error_cls):
            status_code = code
            break

    message = getattr(exc, 'message', str(exc))
    detail = getattr(exc, 'detail', None)

    return JSONResponse(
            status_code=status_code,
            content={
                'message': message,
                'detail': detail,
            }
    )
