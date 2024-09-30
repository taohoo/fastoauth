# -*- coding: utf-8 -*-
"""
@author: hubo
@project: fastframe
@file: oauth_server
@time: 2024/5/23 16:55
@desc:
"""
import uvicorn
from typing import Annotated

from fastoauth import OAuth2
from fastoauth import Token
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


# 在这里调整配置内容。详细说明参考R
# EADME
# OAuth2.SECRET_KEY =
# OAuth2.EXPIRE_SECONDS = 60*60*2
# OAuth2.REDIS_URL = 'redis://localhost:6379/oauth2'


class User(BaseModel):
    """
    创建一个User用来指示Token中包含的数据。
    生成文档用，可能为了灵活性，后续要做修改
    """
    username: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/oauth2/token")
app = FastAPI(docs_url="/oauth2/docs")


@app.post("/oauth2/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """校验账号密码，获取access_token"""
    username = form_data.username
    password = form_data.password
    # 这里添加校验代码
    if username == 'johndoe' and password == 'secret':
        # 这里添加要写入到token中的数据
        return OAuth2.create_access_token({"username": username})
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.post("/oauth2/logout")
async def remove_token(token: Annotated[str, Depends(oauth2_scheme)]):
    """删除服务端缓存的token"""
    OAuth2.remove_token(token)
    return {}


@app.post("/oauth2/refresh_token", response_model=Token)
async def refresh_token(token: Annotated[str, Depends(oauth2_scheme)]):
    """在token过期之前刷新token，无须重新校验账号密码"""
    return OAuth2.refresh_token(token)


@app.get("/oauth2/me", response_model=User)
async def read_users_me(token: Annotated[str, Depends(oauth2_scheme)]):
    """获取缓存在token中用户信息"""
    return OAuth2.get_token_user(token)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()

