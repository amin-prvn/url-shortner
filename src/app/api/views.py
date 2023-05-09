from starlette.datastructures import URL as DataUrl
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request
import validators

from app.api.serializers import URLBaseSerializer, URLAdminSerializer
from app.api.exceptios import http_404, http_400
from app.api.config import get_settings
from app.api.models import URL
from app import main


api = APIRouter()


@api.get("/")   
async def read_root():
    return "Welcome to the URL shortener API :)"


def get_admin_info(db_url: URL) -> URLAdminSerializer:
    base_url = DataUrl(get_settings().BASE_URL)
    admin_endpoint = main.app.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


@api.post("/url", response_model=URLAdminSerializer)
async def create_url(url: URLBaseSerializer):
    if not validators.url(url.target_url):
        http_400(message="Your provided URL is not valid")
    db_url = await URL.create(url=url)
    return get_admin_info(db_url)


@api.get("/{url_key}")
async def forward_to_target_url( url_key: str ,request: Request):
    if url := await URL.get_by_key(url_key=url_key):
        await url.clicked()
        return RedirectResponse(url.target_url)
    else:
        http_404(request)  


@api.get("/admin/{secret_key}", name="administration info", response_model=URLAdminSerializer)
async def get_url_info(secret_key: str, request: Request):
    if url := await URL.get_by_secret_key(secret_key=secret_key):
        return get_admin_info(url)
    else:
        http_404(request)


@api.delete("/admin/{secret_key}")
async def delete_url(secret_key: str, request: Request):
    if url := await URL.get_by_secret_key(secret_key=secret_key):
        await url.deactive()
        message = (
            f"Successfully deleted shortened URL for {url.target_url}"
        )
        return {"detail": message}
    else:
        http_404(request)