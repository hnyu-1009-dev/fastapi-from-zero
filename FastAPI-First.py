# 第一个模块
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# 启动服务
# 1.通过命令 ：uvicon filename:app_name --reload
# (Agent-WorkSpace) PS D:\WorkSystem\fastapi-from-zero> uvicorn FastAPI_Param.pathParam:app --reload
# 如果终端路径不是在当前目录下，应该指定路径
# 关闭终端服务也会关闭
# 2.通过调试模式： fastapi dev filename
# 3.通过py运行: python filename.py

import uvicorn

if __name__ == "__main__":
    uvicorn.run("FastAPI-First:app", host="127.0.0.1", port=8008, reload=True)
