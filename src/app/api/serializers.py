from pydantic import BaseModel


class URLBaseSerializer(BaseModel):
    target_url: str


class URLSerializer(URLBaseSerializer):
    is_active: bool
    clicks: int
    class Config:
        orm_mode = True


class URLAdminSerializer(URLSerializer):
    url: str
    admin_url: str
