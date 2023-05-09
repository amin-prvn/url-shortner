from fastapi import HTTPException


def http_400(message):
    raise HTTPException(status_code=400, detail=message)

def http_404(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)