
from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import RedirectResponse

def not_authorized(request: Request, exc: StarletteHTTPException):
    return RedirectResponse("/users/login")

def not_found(request: Request, exc: StarletteHTTPException):
    return RedirectResponse("/not_found")

def server_error(request: Request, exc: StarletteHTTPException):
    import traceback

    with open("server_errors.txt", "a") as f:
        content = "".join(
            traceback.format_exception(etype=type(exc), value=exc, tb=exc.__traceback__)
        )
        f.write(content)
        f.write('\n\n')
    return RedirectResponse("/server_error")