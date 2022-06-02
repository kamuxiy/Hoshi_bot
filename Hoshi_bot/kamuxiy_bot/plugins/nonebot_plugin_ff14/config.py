from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    kafeapi: str = "https://cafemaker.wakingsands.com"  # 咖啡国服镜像
    xivapi:str = "https://xivapi.com"  # 外网原版

    class Config:
        extra = "ignore"
