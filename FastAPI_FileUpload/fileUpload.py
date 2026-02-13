from fastapi import FastAPI, Path, File, UploadFile
import aiofiles
from enum import Enum
from typing import Annotated
from pydantic import BeforeValidator, BaseModel, Field, field_validator
from uuid import uuid4
import os

app = FastAPI()
# 确保保存目录存在
UPLOAD_DIR = "./data"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload1/")
def upload_file1(file: bytes = File(...)):
    with open("./data/file.jpg", "wb") as f:
        f.write(file)
    return {
        "msg": "文件上传成功",
    }


@app.post("/upload2/")
async def upload_file2(file: UploadFile):
    async with aiofiles.open("./data/{file.filename}.jpg", "wb") as f:
        # chunk = await file.read(1024 * 1024)
        # while chunk:
        #     await f.write(chunk)
        #     chunk = await file.read(1024 * 1024)
        while chunk := await file.read(1024 * 1024):
            await f.write(chunk)
    return {
        "msg": "文件上传成功",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("fileUpload:app", host="127.0.0.1", port=8000, reload=True)
