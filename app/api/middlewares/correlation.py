from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import correlation_id_context


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        correlation_id = request.headers.get(
            "X-Correlation-ID",
            str(uuid4()),
        )

        token = correlation_id_context.set(
            correlation_id,
        )

        try:
            response = await call_next(request)
        finally:
            correlation_id_context.reset(token)

        response.headers["X-Correlation-ID"] = correlation_id

        return response
