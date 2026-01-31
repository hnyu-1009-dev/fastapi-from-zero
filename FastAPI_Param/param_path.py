from fastapi import FastAPI, Path
from enum import Enum
from typing import Annotated
from pydantic import BeforeValidator


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


def validate(value):
    if not value.startswith("P-"):
        raise ValueError("必须以P-开头")
    return value


app = FastAPI()


@app.get("/item1/{item_id}")
def read_item1(item_id: int):
    return {"item_id": item_id}


@app.get("/item2/{item_id}")
def read_item2(item_id: int = Path(...)):
    return {"item_id": item_id}


@app.get("/item3/{item_id}")
def read_item3(item_id: int = Path(..., lt=100, gt=18)):
    return {"item_id": item_id}


@app.get("/item4/{item_id}")
def read_item4(item_id: str = Path(..., regex="^a\d{2}$")):
    """
    Docstring for read_item4

    :param item_id: Description
    :type item_id: str regex 或 pattern
    """
    return {"item_id": item_id}


@app.get("/item5/{model}")
def read_item5(model: ModelName):
    return {"model": model}


# 创建带验证的类型别名
Item = Annotated[str, BeforeValidator(validate)]


@app.get("/item6/{item_id}")
def read_item6(item_id: Item):
    return {"item_id": item_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("param_path:app", host="127.0.0.1", port=8000, reload=True)
