from fastapi import FastAPI, Form
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()


# --- 模式 A：通用模型 (推荐) ---
class User1(BaseModel):
    """
    这是一个纯净的 Pydantic 模型。
    特性：
    1. 解耦：模型本身不关心数据来源（JSON、Form 或数据库查询）。
    2. 复用性：既可以用于 login2(接收表单)，也可以用于其他接收 JSON 的接口。
    """

    username: str
    password: str


# --- 模式 B：专用模型 ---
class User2(BaseModel):
    """
    这是一个与 FastAPI Form 强绑定的模型。
    特性：
    1. 耦合：模型内部指定了数据必须来自 Form。
    2. 限制：该模型几乎只能用于表单接收，失去了作为通用 DTO (数据传输对象) 的灵活性。
    3. 冗余：在接口处仍需 Annotated[User2, Form()] 触发解析逻辑。
    """

    username: str = Form(...)
    password: str = Form(...)


@app.post("/login1/")
def login1(username: str, password: str):
    """直接在函数参数中定义字段，不使用模型。适用于字段极少的情况。"""
    return {"username": username, "password": password}


@app.post("/login2/")
def create_user_2(user: Annotated[User1, Form()]):
    """
    【推荐写法】
    区别：将 User1 这个通用模型“强制”以 Form 格式解析。
    优势：如果你以后想把这个接口改为接收 JSON，只需把 Form() 改成 Body()，
    而不需要去改动 User1 类的定义。
    """
    return user


@app.post("/login3/")
def create_user_3(user: Annotated[User2, Form()]):
    """
    【专用写法】
    区别：User2 内部已经写死了 Form(...)。
    风险：如果此处漏写了 Annotated 中的 Form()，FastAPI 可能会因为模型内部的
    Form 定义与外部默认的 JSON 解析产生冲突，导致接口无法正常工作。
    """
    return user


if __name__ == "__main__":
    import uvicorn

    # 注意：文件名需与此处一致，假设文件名为 main.py
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
