from fastapi import FastAPI, Path
from enum import Enum
from typing import Annotated
from pydantic import BeforeValidator, BaseModel, Field, field_validator
from uuid import uuid4

app = FastAPI()


class User(BaseModel):
    name: str = Field(default="Lubu")
    age: int = Field(...)


class Product(BaseModel):
    price: float = Field(..., gt=0, le=100, description="价格")


class Account(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., pattern="^\w{6,}")


class Item(BaseModel):
    name: str = Field(
        ..., title="商品名称", description="长度不要超过50字符", examples="手机"
    )


class User2(BaseModel):
    email: str

    @field_validator("email")
    def email_validator(cls, v):
        if "@" not in v:
            raise ValueError("邮箱错误")
        return v


class Order(BaseModel):
    items: list = Field(..., min_length=10)
    address: str = Field(..., description="配送地址")


class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Task(BaseModel):
    """
        Docstring for Task
    1.uuid4()

      生成一个随机 UUID（形如：550e8400-e29b-41d4-a716-446655440000），概率上可视为唯一。

    2.default_factory=...

      核心概念：default_factory
      在 Python 类中，如果你直接写 id: str = str(uuid4())，这个函数只会在程序启动、类被加载时运行一次。
      这意味着你创建的所有对象都会拥有同一个 ID，这显然不是我们想要的。

    3.lambda: str(uuid4())

      uuid4() 返回的是 UUID 对象，这里用 str(...) 把它转成字符串，和 id: str 类型一致。
    """

    status: Status = Field(default=Status.ACTIVE)


class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4))


@app.post("/users/")
def create_user(user: User):
    return user


@app.post("/products/")
def create_user(product: Product):
    return product


@app.post("/accounts/")
def create_user(accounts: Account):
    return accounts


@app.post("/user2/")
def creat_user2(user: User2):
    return user


@app.post("/order/")
def create_order(order: Order):
    return order


@app.post("/tasks/")
def crerate_task():
    return Task()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("param_field:app", host="127.0.0.1", port=8000, reload=True)
