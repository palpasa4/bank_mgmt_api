from fastapi.responses import JSONResponse

def json_response(content, status_code: int):
    return JSONResponse(
        content=content,
        status_code=status_code
    )