from fastapi import status

from app.schemas.errors import (
    BadRequestErrorSchema,
    ConflictErrorSchema,
    ForbiddenErrorSchema,
    GoneErrorSchema,
    InternalServerErrorSchema,
    NotFoundErrorSchema,
    UnauthorizedErrorSchema,
)

ERROR_RESPONSES_REGISTRY = {
    status.HTTP_400_BAD_REQUEST: BadRequestErrorSchema,
    status.HTTP_401_UNAUTHORIZED: UnauthorizedErrorSchema,
    status.HTTP_403_FORBIDDEN: ForbiddenErrorSchema,
    status.HTTP_404_NOT_FOUND: NotFoundErrorSchema,
    status.HTTP_409_CONFLICT: ConflictErrorSchema,
    status.HTTP_500_INTERNAL_SERVER_ERROR: InternalServerErrorSchema,
    status.HTTP_410_GONE: GoneErrorSchema,
}


def get_responses(*status_codes: int) -> dict:
    return {
        code: {'model': ERROR_RESPONSES_REGISTRY[code]}
        for code in status_codes
        if code in ERROR_RESPONSES_REGISTRY
    }


GLOBAL_RESPONSES = get_responses(500, 400, 401)
