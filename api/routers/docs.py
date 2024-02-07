from fastapi import APIRouter, Request
from fastapi.openapi.docs import get_swagger_ui_html

__all__ = (
    "router",
)

router = APIRouter()

@router.get("/docs", include_in_schema = False)
async def custom_swagger_ui_html_cdn(request: Request):
    return get_swagger_ui_html(
    title = "aghpb API - Docs", 
    openapi_url = request.app.openapi_url, 
    swagger_favicon_url = "https://raw.githubusercontent.com/THEGOLDENPRO/aghpb_api/main/assets/logo.png",
)