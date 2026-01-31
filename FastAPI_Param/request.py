from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional


# 定义一个 Item 模型，这个模型会被用作请求体的验证和解析
class Item(BaseModel):
    name: str  # 商品名称，必须是字符串
    description: str | None = None  # 商品描述，选填字段，类型是字符串或者 None
    price: float  # 商品价格，必须是浮动类型的数字


# 创建 FastAPI 应用实例
app = FastAPI()


# 定义 POST 路由，接收 Item 类型的请求体
@app.post("/items/")
async def create_item(item: Item):
    """
        接受一个商品信息（Item）作为请求体，并返回该商品数据。
        FastAPI 会自动验证请求体，并将其解析为 Item 对象。
        :param item: 请求体中的 Item 对象
        :return: 返回 Item 对象
        Item 模型：

    1.Item 继承自 pydantic.BaseModel，表示这是一个 Pydantic 模型，用于数据验证和解析。

      - name: 是一个必需的字符串字段。
      -
      - description: 是一个可选的字符串字段，可以为空（None）。
      -
      - price: 是一个必需的浮动数字类型。

    2.create_item 路由：

      - @app.post('/items/') 指定了这个路由处理 POST 请求。
      -
      - 函数参数 item: Item 会告诉 FastAPI 从请求体中提取 JSON 数据，并自动将其解析为 Item 类型。FastAPI 会在请求体中查找与 Item 模型匹配的字段，并进行类型验证。

    如果请求体数据不符合 Item 模型，FastAPI 会返回一个 422 错误，提示数据格式不正确。
    """
    return item  # 返回解析的 Item 对象


# 请求体模型使用 Optional 和 default：


class Product(BaseModel):
    name: str
    description: Optional[str] = Field(None, max_lenth=100)
