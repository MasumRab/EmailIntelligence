
from fastapi import Request, status
from fastapi.responses import JSONResponse

class DatabaseErrorHandler:
    @staticmethod
    async def handle(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "A database error occurred."},
        )

class GmailServiceErrorHandler:
    @staticmethod
    async def handle(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "A Gmail service error occurred."},
        )

class GeneralErrorHandler:
    @staticmethod
    async def handle(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An unexpected error occurred."},
        )
